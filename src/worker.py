"""
Worker Module

Worker runs work.
"""
import os
import requests
from multiprocessing.context import Process
from enum import Enum
from retrying import retry

from src.exceptions import ExtractException, ComparisionException, UploadS3Exception, GetTotalScoreException, CallApiSuccessException, CallApiFailException, InvalidWorkException
import src.log as log
from src.json_reader import AnalysesJsonReader

class WorkerResolveStatus(Enum):
    """
    dddd
    """
    SUCCESS = 1
    FAIL_EXTRACTION = 2
    FAIL_COMPARISION = 3
    FAIL_UPLOAD = 4
    FAIL_SCORE = 5
    FAIL_CALL_API = 6
    FAIL = 7

class APIStatusCode(Enum):
    SUCCESS = '120003'
    FAIL = '120004'

class APIGradeCode(Enum):
    S = '50001'
    A = '50002'
    B = '50003'
    C = '50004'
    D = '50005'

    @staticmethod
    def loads(score: int):
        if 100 >= score >=95:
            return APIGradeCode.S
        elif 95 > score >= 90:
            return APIGradeCode.A
        elif 90 > score >= 85:
            return APIGradeCode.B
        elif 85 > score >= 80:
            return APIGradeCode.C

class CMDExitCode(Enum):
    SUCCESS = 0
    FAILED = 1
    NOT_HANDLED = 2

    @staticmethod
    def loads(cmd_output: str):
        if 'success' in cmd_output:
            return CMDExitCode.SUCCESS
        elif 'failed' in cmd_output:
            return CMDExitCode.FAILED
        return CMDExitCode.NOT_HANDLED

def parse_sec(raw_sec: str) -> int:
    raw_time = int(raw_sec.split(':')[0])
    raw_min = int(raw_sec.split(':')[1])
    raw_sec = int(raw_sec.split(':')[2])

    SEC_PER_TIME = 3600
    SEC_PER_MIN = 60

    return raw_time*SEC_PER_TIME + raw_min*SEC_PER_MIN + raw_sec

class Work:
    MAX_RETRY = 3
    RETRY_WAIT = 1
    def __init__(self, body, jwt):
        try: 
            self.an_seq = body['an_seq']
            self.user_video_filename = body['user_video_filename']
            self.user_sec = parse_sec(body['user_sec'])
            self.ref_json_filename = body['ref_json_filename']
            self.ref_sec = parse_sec(body['ref_sec'])
            self.retry_times = 0
            self.jwt = jwt
        except:
            raise InvalidWorkException(f'Invalid Work format.\n args: {body}, {jwt}')
    
            

class Worker(Process):
    def __init__(self, work: Work):
        super(Worker, self).__init__()
        self.work: Work = work

    def resolve(self) -> WorkerResolveStatus:
        try:
            log.info(f'[{os.getpid()}] Started work')
            ext_file = self.__extract()
            self.__get_ref_json()
            an_file = self.__comparison(ext_file)
            total_score = self.__get_total_score(an_file)
            self.__uploadS3(ext_file, an_file)
            self.__call_api_success(an_file, ext_file, total_score)
            self.__clear_dir()
            log.info(f'[{os.getpid()}] Successfully finished work')
            return WorkerResolveStatus.SUCCESS
            
        except ExtractException as e:
            log.error(e)
            self.__call_api_fail()
            return WorkerResolveStatus.FAIL_EXTRACTION

        except ComparisionException as e:
            log.error(e)
            self.__call_api_fail()
            return WorkerResolveStatus.FAIL_COMPARISION

        except UploadS3Exception as e:
            log.error(e)
            self.__call_api_fail()
            return WorkerResolveStatus.FAIL_UPLOAD

        except GetTotalScoreException as e:
            log.error(e)
            self.__call_api_fail()
            return WorkerResolveStatus.FAIL_SCORE

        except CallApiSuccessException as e:
            log.error(e)
            self.__call_api_fail()
            return WorkerResolveStatus.FAIL_CALL_API

        except CallApiFailException as e:
            log.error(e)
            self.__call_api_fail()
            return WorkerResolveStatus.FAIL_CALL_API

        except Exception as e:
            log.error(e.with_traceback())
            self.__call_api_fail()
            return WorkerResolveStatus.FAIL

    @retry(stop_max_attempt_number=Work.MAX_RETRY, wait_fixed=Work.RETRY_WAIT)
    def __extract(self):
        log.info(f'[{os.getpid()}] Extracting From {self.work.user_video_filename}')

        script_dir = os.getenv('ROOT_DIR')+'/scripts'
        extraction_cmd = f'bash {script_dir}/extract.sh {self.work.user_video_filename}'
        result: str = os.popen(extraction_cmd).read()
        log.info(f'[{os.getpid()}] Extraction cmd output: {result}')

        status = CMDExitCode.loads(result)

        if status == CMDExitCode.FAILED:
            raise ExtractException(
                f'[{os.getpid()}] Failed to extract From {self.work.user_video_filename}\n' + \
                f'console output: {result}'
            )
        if status == CMDExitCode.NOT_HANDLED:
            raise ExtractException(
                f'[{os.getpid()}] Not handled error occured while extracting From {self.work.user_video_filename}\n' + \
                f'console output: {result}'
            )
        
        extracted_filename = self.work.user_video_filename.split('.')[0] + '_l2norm.json'
        
        return extracted_filename

    @retry(stop_max_attempt_number=Work.MAX_RETRY, wait_fixed=Work.RETRY_WAIT)  
    def __get_ref_json(self):
        s3_bucket = os.getenv('REF_JSON_S3_BUCKET')
        ref_json_path = os.getenv('REF_JSON_PATH')
        ref_json_filename = self.work.ref_json_filename

        log.info(f'[{os.getpid()}] Downloading {s3_bucket}/{ref_json_filename} to {ref_json_path}/{ref_json_filename}')
        script_dir = os.getenv('ROOT_DIR')+'/scripts'
        download_cmd = f'bash {script_dir}/download_ref_json.sh {ref_json_filename}'
        result: str = os.popen(download_cmd).read()
        log.info(f'[{os.getpid()}] Download cmd output: {result}')

        status = CMDExitCode.loads(result)

        if status == CMDExitCode.FAILED:
            raise ExtractException(
                f'[{os.getpid()}] Failed to download ref json From {s3_bucket}/{ref_json_filename} to {ref_json_path}/{ref_json_filename}\n' + \
                f'console output: {result}'
            )
        if status == CMDExitCode.NOT_HANDLED:
            raise ExtractException(
                f'[{os.getpid()}] Not handled error occured while downloading ref json From {s3_bucket}/{ref_json_filename} to {ref_json_path}/{ref_json_filename}\n' + \
                f'console output: {result}'
            )
        
        extracted_filename = self.work.user_video_filename.split('.')[0] + '_l2norm.json'
        
        return extracted_filename

    @retry(stop_max_attempt_number=Work.MAX_RETRY, wait_fixed=Work.RETRY_WAIT)
    def __comparison(self, extracted_filename: str):
        log.info(f'[{os.getpid()}] Comparing {extracted_filename}(usr) to {self.work.ref_json_filename}(ref)')

        ref_json_path = os.getenv('REF_JSON_PATH')
        script_dir = os.getenv('ROOT_DIR')+'/scripts'
        comparison_cmd = f'bash {script_dir}/comparison.sh {extracted_filename} {self.work.user_sec} {ref_json_path}/{self.work.ref_json_filename} {self.work.ref_sec}'
        result: str = os.popen(comparison_cmd).read()

        log.info(f'[{os.getpid()}] Compare cmd output: {result}')

        status = CMDExitCode.loads(result)

        if status == CMDExitCode.FAILED:
            raise ExtractException(
                f'[{os.getpid()}] Failed to compare {extracted_filename}(usr) to {self.work.ref_json_filename}(ref)\n' + \
                f'console output: {result}'
            )
        if status == CMDExitCode.NOT_HANDLED:
            raise ExtractException(
                f'[{os.getpid()}] Not handled error occured while comparing {extracted_filename}(usr) to {self.work.ref_json_filename}(ref)\n' + \
                f'console output: {result}'
            )

        no_ext = extracted_filename.split('_l2')[0]
        analysis_filename = f'{no_ext}_analysis.json'

        return analysis_filename

    @retry(stop_max_attempt_number=Work.MAX_RETRY, wait_fixed=Work.RETRY_WAIT)
    def __uploadS3(self, extracted_name: str, analysis_name: str):
        log.info(f'[{os.getpid()}] Uploading {extracted_name}, {analysis_name} to S3 bucket')

        script_dir = os.getenv('ROOT_DIR')+'/scripts'

        upload_cmd = f'bash {script_dir}/upload_s3.sh {extracted_name} {analysis_name}'
        result = os.popen(upload_cmd).read()
        log.info(f'[{os.getpid()}] Upload cmd output: {result}')

        status = CMDExitCode.loads(result)

        if status == CMDExitCode.FAILED:
            raise ExtractException(
                f'[{os.getpid()}] Failed to upload {extracted_name}, {analysis_name} to S3 bucket\n' + \
                f'console output: {result}'
            )
        if status == CMDExitCode.NOT_HANDLED:
            raise ExtractException(
                f'[{os.getpid()}] Not handled error occured while uploading {extracted_name}, {analysis_name} to S3 bucket\n' + \
                f'console output: {result}'
            )

    @retry(stop_max_attempt_number=Work.MAX_RETRY, wait_fixed=Work.RETRY_WAIT)
    def __get_total_score(self, an_file) -> int:
        log.info(f'[{os.getpid()} Getting totalscore from an_file')
        file_path = str(os.getenv('AN_JSON_PATH')) + f'/{an_file}'
        try:
            reader = AnalysesJsonReader(file_path)
            total_score = reader.get_total_score()
            return total_score
        except Exception as e:
            raise GetTotalScoreException(f'Failed to get total score from filename {an_file}') from e


    @retry(stop_max_attempt_number=Work.MAX_RETRY, wait_fixed=Work.RETRY_WAIT)
    def __call_api_success(self, an_file, ext_file, total_score):
        log.info(f'[{os.getpid()}] Calling ApiSuccess anSeq {self.work.an_seq}')
        URL = os.getenv('API_URL')+'/analyses/result'
        response = requests.put(URL, json={
            "anSeq": self.work.an_seq,
            "anScore": total_score,
            "anGradeCode": "50001",
            "anUserVideoMotionDataFilename": ext_file,
            "anSimularityFilename": an_file,
            "anStatusCode": "120001"
        }, headers={
            "Authorization": self.work.jwt
        })

        if response.status_code != 200:
            raise CallApiSuccessException(f'[{os.getpid()}] API request Failed. body:{response}')
        print(response)

    @retry(stop_max_attempt_number=Work.MAX_RETRY, wait_fixed=Work.RETRY_WAIT)
    def __call_api_fail(self):
        print(f'[{os.getpid()}] Calling ApiFail anSeq {self.work.an_seq}')
        URL = os.getenv('API_URL')+'/analyses/result'
        response = requests.put(URL, json={
            "anSeq": self.work.an_seq,
            "anScore": 0,
            "anGradeCode": "50001",
            "anUserVideoMotionDataFilename": "",
            "anSimularityFilename": "",
            "anStatusCode": "120004"
        }, headers={
            "Authorization": self.work.jwt
        })
        if response.status_code != 200:
            raise CallApiSuccessException(f'[{os.getpid()}] API request Failed. body:{response}')
        print(response)

    def __clear_dir(self):
        pass

if __name__ == '__main__':
    jwt = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtYnJTZXEiOiIxIiwiZXhwIjoxNjM0MTI5ODQxLCJhY2Nlc3NUb2tlbiI6Ik5LQmlHQWNZQ2ViZFlXMEt1VkpEZDVLODFjWk03VmEyaEFKNHh3b3BiN2tBQUFGOGVIRDRVdyIsImlhdCI6MTYzNDEwODI0Mn0.4kt1bEndNSP_VWpwz7FC8qgczscNAGGglbsyXFi8Ils'
    work = Work({
        "an_seq": "8", 
        "user_video_filename": "wannabe_kakao_vertical.mp4",
        "user_sec": "00:00:33",
        "ref_json_filename": "지구에이어아이들을지키러온츄의월드이즈원츄챌린지Shorts_엠뚜루마뚜루MBC공식종합채널_l2norm.json",
        "ref_sec": "00:00:25"
    },
    jwt)
    worker = Worker(work)
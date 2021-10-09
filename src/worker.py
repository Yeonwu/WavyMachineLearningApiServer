"""
Worker Module

Worker runs work.
"""
from multiprocessing.context import Process
from multiprocessing.queues import Queue
import os
import sys
from time import sleep
from enum import Enum

from src.exceptions import CallApiFailException, CallApiSuccessException, ComparisionException, ExtractException, InvalidWorkException, UploadS3Exception

class WorkerResolveStatus(Enum):
    """
    dddd
    """
    SUCCESS = 1,
    FAIL_EXTRACTION = 2,
    FAIL_COMPARISION = 3,
    FAIL_UPLOAD = 4,
    FAIL_CALL_API = 5,
    FAIL = 6

class CMDExitCode(Enum):
    SUCCESS = 0,

    @staticmethod
    def loads(cmd_output):
        return 0

class Work:
    MAX_RETRY = 3
    def __init__(self, body):
        try: 
            self.an_seq = body['an_seq']
            self.user_video_filename = body['user_video_filename']
            self.user_sec = body['user_sec']
            self.ref_json_filename = body['ref_json_filename']
            self.ref_sec = body['ref_sec']
            self.retry_times = 0
        except Exception as exc:
            raise InvalidWorkException() from exc


    def is_max_retry(self) -> bool:
        if self.retry > Work.MAX_RETRY:
            return False
        return True

    def retry(self):
        self.retry_times += 1
        return self
            

class Worker(Process):
    def __init__(self, work: Work):
        super(Worker, self).__init__()
        self.work: Work = work

    def resolve(self) -> WorkerResolveStatus:
        try:
            print(f'{os.getpid()}')
            extracted_name = self.__extract()
            analysis_name = self.__comparison(extracted_name)
            self.__uploadS3(extracted_name, analysis_name)
            self.__call_api_success()
            return WorkerResolveStatus.SUCCESS
            
        except ExtractException as e:
            self.__retry()
            return WorkerResolveStatus.FAIL_EXTRACTION

        except ComparisionException as e:
            self.__retry()
            return WorkerResolveStatus.FAIL_COMPARISION

        except UploadS3Exception as e:
            self.__retry()
            return WorkerResolveStatus.FAIL_UPLOAD

        except CallApiSuccessException as e:
            self.__retry()
            return WorkerResolveStatus.FAIL_CALL_API

        except CallApiFailException as e:
            self.__log()
            return WorkerResolveStatus.FAIL_CALL_API

        except:
            self.__log()
            return WorkerResolveStatus.FAIL

    def __extract(self):
        print(f'{os.getpid()}: Extracting From {self.work.user_video_filename}')

        script_dir = os.getenv('ROOT_DIR')+'/scripts'
        extraction_cmd = f'sh {script_dir}/extract.sh {self.work.user_video_filename}'
        result: str = os.popen(extraction_cmd).read()
        
        extracted_filename = self.work.user_video_filename.split('.')[0] + '.json'
        
        return extracted_filename

    def __comparison(self, extracted_filename: str):
        print(f'{os.getpid()}: Comparing {extracted_filename}(usr) to {self.work.ref_json_filename}(ref)')

        script_dir = os.getenv('ROOT_DIR')+'/scripts'
        comparison_cmd = f'sh {script_dir}/comparison.sh {extracted_filename} {self.work.user_sec} {self.work.ref_json_filename} {self.work.ref_sec}'
        result: str = os.popen(comparison_cmd).read()

        no_ext = extracted_filename.split('.')[0]
        analysis_filename = f'/analyzes/{no_ext}_analysis.json'

        return analysis_filename


    def __uploadS3(self, extracted_name: str, analysis_name: str):
        print(f'{os.getpid()}: Uploading {extracted_name}, {analysis_name} to S3 bucket')
        sleep(2)

    def __call_api_success(self):
        print(f'{os.getpid()}: Calling ApiSuccess anSeq {self.work.an_seq}')
        sleep(2)

    def __call_api_fail(self):
        print(f'{os.getpid()}: Calling ApiFaile anSeq {self.work.an_seq}')
        sleep(2)

    def __retry(self):
        if self.work.is_max_retry():
            self.__call_api_fail()

    def __log(self):
        pass

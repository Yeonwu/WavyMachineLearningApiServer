import json
from exceptions import JsonLoadException, ScoreCalculateException

class AnalysesJsonReader:
    def __init__(self, file):
        self.file = file

    def get_total_score(self):
        analysis: list = self.__read_file()
        total_score = self.__calculate_total_score(analysis)
        return total_score

    def __read_file(self):
        try:
            f = open(self.file, 'r', encoding='utf8')
            raw_json = f.read()
            parsed_json = json.loads(raw_json)
            return parsed_json['analyzes']
        except Exception as e:
            raise JsonLoadException(f'Failed to load json from file name {self.file}') from e

    def __calculate_total_score(self, analysis: list) -> int:
        try:
            total = 0
            for analysis_second in analysis:
                total += analysis_second['average_score']
            
            avg = round(total / len(analysis))
            return avg
        except Exception as e:
            raise ScoreCalculateException(f'Failed to calculate total score from file name {self.file}') from e


def test():
    file = '/Users/oyeonwu/Desktop/user-video-2021-10-17T08-00-20_analysis.json'
    reader = AnalysesJsonReader(file)
    total_score = reader.get_total_score()
    print(total_score)


if __name__ == '__main__':
    test()
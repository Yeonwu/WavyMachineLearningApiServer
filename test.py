from src.worker import Worker, Work

if __name__ == '__main__':
    jwt = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtYnJTZXEiOiI3IiwiZXhwIjoxNjM1MjUzMDA0LCJhY2Nlc3NUb2tlbiI6InVCMlEzOTN2MFpJZWF3S2RJMFM2bUZ5b01DakpHYjFHbXoycmpBb3BiN2dBQUFGOHUyTVdaUSIsImlhdCI6MTYzNTIzMTQwNX0.HKqASM6yOq1-u7-66N_yee6ZWloceB6JrsrTWKzQww8'
    work = Work({
        "an_seq": "70", 
        "user_video_filename": "wannabe_kakao_vertical.mp4",
        "user_sec": "00:00:33",
        "ref_json_filename": "지구에이어아이들을지키러온츄의월드이즈원츄챌린지Shorts_엠뚜루마뚜루MBC공식종합채널_l2norm.json",
        "ref_sec": "00:00:25"
    },
    jwt)
    worker = Worker(work)
    worker.test()
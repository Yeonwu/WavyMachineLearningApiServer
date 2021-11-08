<div align=center>

<img width="200px" src="https://user-images.githubusercontent.com/26461307/139542520-eb45acd7-48fa-4189-a39e-f10d058c70c8.png"/> <br/>

# Wavy - MachineLearning API Server

인공지능 기반의 맞춤형 K-POP 댄스 학습 서비스

</div>

<div align="center">
  <a href="#introduction">Introduction</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#features">Features</a> •
  <a href="#developer">Developer</a>
</div>

<br/><br/><br/><br/><br/>

## Introduction

<div align="left">

<img alt="Flask" src="https://img.shields.io/badge/-Flask-000000?style=flat-square&logo=flask&logoColor=white" />
<img alt="Python" src="https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white" />
<img  src="https://img.shields.io/badge/AWS S3-569A31?style=flat-square&logo=amazon-s3&logoColor=white" />
<img  src="https://img.shields.io/badge/AWS SDK-232F3E?style=flat-square&logo=amazon-aws&logoColor=white" />

</div>

Wavy MachineLearning API 서버는 Flask를 기반으로 위 개발 스택을 사용하였습니다.  
사용자 영상 분석을 위한 분석 요청을 처리하여 [인공지능 스크립트](https://github.com/EO2-WAVY/WavyMachineLearning)를 실행시키기 위해 개발했습니다.

## Getting Started

[**Wavy**](https://www.wavy.dance)는 [www.wavy.dance](https://www.wavy.dance)에서 만나보실 수 있습니다.

### Project Clone

```bash
git clone https://github.com/EO2-WAVY/WavyMachineLearningApiServer.git
```

### Install Packages

```bash
pip install -r requirements.txt
```

### Environment

`.env`에 환경변수를 설정해주세요.

```bash
FLASK_APP=app.py
FLASK_ENV=development
ROOT_DIR=[프로젝트 루트 디렉토리]
# /log안에는 flask-debug.log, flask-error.log 파일을 만들어주세요.
LOG_DIR=[로그 디렉토리]

CPU_CORE=[한번에 사용할 CPU 코어 개수]
PORT=[Flask 서버 포트]

ML_VENV_PATH=[인공지능 스크립트 가상환경 경로]
ML_PYTHON_SCRIPT_PATH=[인공지능 스크립트 경로]
ML_RUN_PATH=[인공지능 스크립트 실행 경로]

REF_JSON_S3_BUCKET=[비교에 사용할 영상 JSON 버킷명]
REF_JSON_PATH=[위 JSON 다운로드 경로]

EXT_JSON_S3_BUCKET=[사용자 모션 JSON을 업로드할 버킷명]
EXT_JSON_PATH=[사용자 모션 JSON이 저장되어있는 경로]

AN_JSON_S3_BUCKT=[분석 결과 JSON을 업로드할 버킷명]
AN_JSON_PATH=[분석결과 JSON이 저장되어있는 경로]

API_URL=[분석이 완료된 후 호출할 API]

```

### 어플리케이션 실행

```bash
python3 app.py
```

## Features

### Directory Structure

```bash
/
├── scripts
│   └── [Shell script files]
├── src
│   └── [Python files]
├── .env
├── app.py
└── requerments.txt


```

### Packages

```bash
astroid==2.8.2
certifi==2021.10.8
charset-normalizer==2.0.6
click==8.0.1
Flask==2.0.2
idna==3.2
isort==5.9.3
itsdangerous==2.0.1
Jinja2==3.0.2
lazy-object-proxy==1.6.0
MarkupSafe==2.0.1
mccabe==0.6.1
platformdirs==2.4.0
pylint==2.11.1
python-dotenv==0.19.0
requests==2.26.0
retrying==1.3.3
six==1.16.0
toml==0.10.2
typing-extensions==3.10.0.2
urllib3==1.26.7
waitress==2.0.0
Werkzeug==2.0.2
wrapt==1.12.1
```

## Developer

해당 프로젝트는 [소프트웨어 마에스트로](https://www.swmaestro.org/sw/main/main.do) 사업의 지원을 받아 개발되었습니다.

|                               FE: [hyesungoh](https://github.com/hyesungoh)                               |                              AI: [haeseoklee](https://github.com/haeseoklee)                              |                                  BE: [Yeonwu](https://github.com/Yeonwu)                                  |
| :-------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------: |
| <img src="https://avatars.githubusercontent.com/u/26461307?v=4" width="70px" style="border-radius:50%" /> | <img src="https://avatars.githubusercontent.com/u/20268101?v=4" width="70px" style="border-radius:50%" /> | <img src="https://avatars.githubusercontent.com/u/61102178?v=4" width="70px" style="border-radius:50%" /> |

## License

Wavy는 [MIT](https://choosealicense.com/licenses/mit/)라이선스를 따릅니다.

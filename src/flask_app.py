from http import HTTPStatus
import json
from flask import Flask, request, Response
from dotenv import load_dotenv
from multiprocessing import Queue
from src.worker import InvalidWorkException, Work
import src.log as log

load_dotenv(verbose=True)

class FlaskWrapper(Flask):
    app = Flask(__name__)
    queue = None

    @staticmethod
    def set_queue(work_queue: Queue):
        FlaskWrapper.queue = work_queue

app = FlaskWrapper.app

@app.route('/', methods=['POST'])
def register_work_to_queue():
    try:
        body = request.get_json()
        jwt = request.headers.get('Authorization')
        log.info(f'Request body: {body}, {jwt}')

        work = Work(body, jwt)
        FlaskWrapper.queue.put(work)
        response_body = json.dumps({
            "message": 'Successfuly started analysis',
        })
        return Response(response_body, status=HTTPStatus.ACCEPTED)
        
    except InvalidWorkException as e:
        log.error(e.with_traceback())
        response_body = json.dumps({
            "message": 'Invalid request body'
        })
        return Response(response_body, status=HTTPStatus.BAD_REQUEST)

    except Exception as e:
        log.error('Unhandled error occured.')
        log.error(e.with_traceback())
        response_body = json.dumps({
            "message": 'Internal Error'
        })
        return Response(response_body, status=HTTPStatus.INTERNAL_SERVER_ERROR)

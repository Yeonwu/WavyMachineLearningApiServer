from multiprocessing import Pool, Queue, Process
from time import sleep
from waitress import serve
from src.flask_app import FlaskWrapper
from src.worker import Work, Worker
import os

def resolve_work(queue: Queue):
    while True:
        if not queue.empty():
            work = queue.get()
            Worker(work).resolve()

if __name__ == '__main__':
    work_queue = Queue()

    cpu_core = int(os.getenv('CPU_CORE'))
    pool = Pool(cpu_core, initializer=resolve_work, initargs=(work_queue, ))

    FlaskWrapper.set_queue(work_queue)
    serve(FlaskWrapper.app, port=80)

    
from multiprocessing import Pool, Queue
from waitress import serve
import os
from sys import exit
from src.flask_app import FlaskWrapper
from src.worker import Worker
import src.log as log

def resolve_work(queue: Queue):
    log.info(f'[{os.getpid()}] Starting worker process.')
    try:
        log.info(f'[{os.getpid()}] Listening to queue.')
        while True:
            if not queue.empty():
                work = queue.get()
                Worker(work).resolve()
    except Exception as e:
        log.error(f'[{os.getpid()}] Failed to start worker process.')
        log.error(e.with_traceback())


if __name__ == '__main__':
    log_dir = os.getenv('LOG_DIR')
    log.init(log_dir)

    log.info('Flask Process Started.')

    try:
        log.info('Creating Queue.')
        work_queue = Queue()
        log.info('Succesfully created Queue.')
    except Exception as e:
        log.error('Failed to Create Queue.')
        log.error(e.with_traceback())
        exit(1)

    try:
        log.info('Creating Pool.')
        cpu_core = int(os.getenv('CPU_CORE'))
        pool = Pool(cpu_core, initializer=resolve_work, initargs=(work_queue, ))
        log.info('Succesfully Created Pool.')
    except Exception as e:
        log.error('Failed to Create Pool.')
        log.error(e.with_traceback())
        exit(1)

    try:
        log.info('Starting Server.')
        listen_port = os.getenv('PORT')
        FlaskWrapper.set_queue(work_queue)
        serve(FlaskWrapper.app, port=listen_port)

    except Exception as e:
        log.error('Failed to start server.')
        log.error(e.with_traceback())
        exit(1)

    
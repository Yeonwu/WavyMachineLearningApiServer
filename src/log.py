import logging
from datetime import datetime, timezone, timedelta

def init(log_dir: str):
    logging.basicConfig(filename=f'{log_dir}/flask-debug.log', level=logging.INFO)
    logging.basicConfig(filename=f'{log_dir}/flask-error.log', level=logging.CRITICAL)

def __get_date_now():
    return datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')

def __make_msg(msg: str):
    log_date = __get_date_now()
    return ' {0} - {1}'.format(log_date, msg)

def info(msg: str):
    log_msg = __make_msg(msg)
    logging.info(log_msg)

def error(msg: str):
    log_msg = __make_msg(msg)
    logging.error(log_msg)
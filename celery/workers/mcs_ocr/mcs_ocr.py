
import requests
import json
import os

from celery import Celery
from celery.utils.log import get_task_logger

DEBUG_ENDPOINT = 'http://10.44.4.244:5000/ocr/v3'
DEBUG_JSON = '{"url": "http://favim.com/orig/201105/28/hate-life-people-simple-text-typography-Favim.com-57610.jpg"}'

DEBUG_OUTPUT_FOLDER = '_Output'

logger = get_task_logger(__name__)
app = Celery('mcd_ocr', broker='pyamqp://guest@localhost//')


@app.task(name='workers.mcd_ocr.mcd_ocr', queue='mcs_ocr')
def mcs_ocr(*args, **kwargs):
    headers = {'Content-Type': 'application/json'}
    r = requests.post(DEBUG_ENDPOINT, data=DEBUG_JSON, headers=headers)
    logger.info(r.status_code)

    data = r.json()
    logger.info(data)

    return (args, kwargs)

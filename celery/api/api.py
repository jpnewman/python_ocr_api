
from kombu import Queue
from celery import subtask
from celery import Celery, chain
from celery.utils.log import get_task_logger

from workers.find_regions.find_regions import find_regions
from workers.debug_regions.debug_regions import debug_regions
from workers.mcs_ocr.mcs_ocr import mcs_ocr
from workers.validate_address.validate_address import validate_address

logger = get_task_logger(__name__)

app = Celery('tasks', broker='pyamqp://guest@localhost//')
app.conf.task_default_queue = 'default'
app.conf.task_queues = (
    Queue('find_regions',    routing_key='find_regions'),
    Queue('debug_regions', routing_key='debug_regions'),
    Queue('mcs_ocr',    routing_key='mcs_ocr'),
    Queue('validate_address', routing_key='validate_address')
)
task_default_exchange = 'tasks'
task_default_exchange_type = 'topic'
task_default_routing_key = 'task.default'

def ocr_pipeline(user_token, doc_id):
    data = {
        'user_token': user_token,
        'doc_id': doc_id
    }

    # find_regions.delay(data)
    # debug_regions.delay(data)
    # validate_address.delay(data)
    # mcs_ocr.delay(data)

    # ret = chain(find_regions.s(data).set(queue='find_regions'),
    #             mcs_ocr.s().set(queue='mcs_ocr'),
    #             debug_regions.s().set(queue='debug_regions'),
    #             validate_address.s().set(queue='validate_address')).apply_async()

    ret = chain(mcs_ocr.s(data).set(queue='mcs_ocr'),
                debug_regions.s().set(queue='debug_regions'),
                validate_address.s().set(queue='validate_address')).apply_async()

    logger.debug(ret)


from celery import Celery, chain
from celery.utils.log import get_task_logger

from workers.find_regions.find_regions import find_regions
from workers.debug_regions.debug_regions import debug_regions
from workers.validate_address.validate_address import validate_address

logger = get_task_logger(__name__)

app = Celery('tasks', broker='pyamqp://guest@localhost//')


def ocr_pipeline(doc_id):
    data = {
        'doc_id': doc_id
    }

    # validate_address.delay(data)

    ret = chain(find_regions.s(data), debug_regions.s(), validate_address.s()).apply_async()
    logger.debug(ret)

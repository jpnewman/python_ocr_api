import os
import requests
import json

from AddressCompare import get_address_scan

from celery import Celery
from celery.utils.log import get_task_logger

DEBUG_FIRSTNAME = u'John'
DEBUG_SURNAME = u'Stein'
DEBUG_POSTCODE_END = u'2RX'

logger = get_task_logger(__name__)
app = Celery('validate_address', broker='pyamqp://guest@localhost//')


@app.task(name='workers.validate_address.validate_address', queue='validate_address')
def validate_address(*args, **kwargs):
    logger.info(args[0])
    address = get_address_scan(DEBUG_FIRSTNAME,
                               DEBUG_SURNAME,
                               DEBUG_POSTCODE_END,
                               args[0][0][0]['mcs_data']) # FIX: arg get boxed with each call

    # Validate address
    logger.debug(address)
    url_addr = "https://maps.googleapis.com/maps/api/geocode/json"
    payload = {'address': address, 'key': 'AIzaSyBRpWc0C_DvxiGfaOu5fITfJgsqPWzevm0'}
    res = requests.get(url_addr, params=payload)
    logger.debug(res.url)
    out = res.json()
    logger.debug(out)

    google_address = ''
    match = ''
    partial_match = False
    if len(out['results']):
        google_address = out['results'][0]['formatted_address']

        if out['results'][0].has_key('partial_match'):
            partial_match = out['results'][0]['partial_match']

    logger.info("{0} : {1}".format(google_address, partial_match))

    # return google_address, partial_match

    return args

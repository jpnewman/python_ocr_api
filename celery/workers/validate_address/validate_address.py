import os
import requests
import json

from AddressCompare import get_address_scan

from celery import Celery
from celery.utils.log import get_task_logger

DEBUG_FIRSTNAME = u'John'
DEBUG_SURNAME = u'Stein'
DEBUG_POSTCODE_END = u'2RX'

# DEBUG_REGIONS = '../../_TestData/Microsoft_computer-vision-api/bgbill12/bgbill12.json'
DEBUG_REGIONS = '../../_TestData/Microsoft_computer-vision-api/validate_address/billsample.json'

logger = get_task_logger(__name__)
app = Celery('validate_address', broker='pyamqp://guest@localhost//')


@app.task(name='workers.validate_address.validate_address', queue='validate_address')
def validate_address(*args, **kwargs):
    address = get_address_scan(DEBUG_FIRSTNAME, DEBUG_SURNAME, DEBUG_POSTCODE_END, os.path.expanduser(DEBUG_REGIONS))
    # google_address, match = validate_address(address)

    logger.info(address)
    url_addr = "https://maps.googleapis.com/maps/api/geocode/json"
    payload = {'address': address, 'key': 'AIzaSyBRpWc0C_DvxiGfaOu5fITfJgsqPWzevm0'}
    res = requests.get(url_addr, params=payload)
    logger.info(res.url)
    out = res.json()
    print(out)

    google_address = ''
    match = ''
    if len(out['results']):
        google_address = out['results'][0]['formatted_address']

        partial_match = False
        if out['results'][0].has_key('partial_match'):
            partial_match = out['results'][0]['partial_match']

    logger.info("{0} : {1}".format(google_address, partial_match))

    # return google_address, partial_match

    return (args, kwargs)

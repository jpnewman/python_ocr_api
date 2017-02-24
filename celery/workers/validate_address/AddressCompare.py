# Author: Geoff Clark

import json
import requests

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

GOOGLE_API_KEY = '<YOUR_GOOGLE_API_KEY>'

def get_address_scan(firstname, surname, postcode_end, scan_file):
    logger.info(firstname)
    logger.info(surname)
    logger.info(postcode_end)
    logger.info(scan_file)

    with open(scan_file, "r") as f:
        regions = json.loads(f.read())

    logger.info(regions)

    address = u''
    capture = 0
    for region in regions['regions']:
        for line in region['lines']:
            for word in line['words']:
                if word["text"].lower() == firstname.lower() or word[
                    "text"].lower() == surname.lower() and capture == 0:
                    capture = 1
                if capture == 1:
                    # logic below excludes name if at beginning of address
                    if not (address == u'' and (
                            word["text"].lower() == firstname.lower() or word["text"].lower() == surname.lower())):
                        address = address + word["text"] + u' '
                if word["text"].lower() == postcode_end.lower():
                    capture = 2
                if capture == 2:
                    break
            if capture == 2:
                break
        if capture == 2:
            break


    logger.info("Addr: {0}".format(address))
    return address


def validate_address(address):
    logger.info(address)
    url_addr = "https://maps.googleapis.com/maps/api/geocode/json"
    payload = {'address': address, 'key': GOOGLE_API_KEY}
    res = requests.get(url_addr, params=payload)
    logger.info(res.url)
    out = res.json()
    print(out)

    results = ''
    match = ''
    if len(out['results']):
        results = out['results'][0]['formatted_address']
        match = out['results'][0]['partial_match']

    return results, match

# Author: Geoff Clark

import json
import requests

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

GOOGLE_API_KEY = '<YOUR_GOOGLE_API_KEY>'

def get_address_scan(firstname, surname, postcode_end, scan_file):
    logger.debug(firstname)
    logger.debug(surname)
    logger.debug(postcode_end)
    logger.debug(scan_file)

    with open(scan_file, "r") as f:
        regions = json.loads(f.read())

    logger.debug(regions)

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

    return address

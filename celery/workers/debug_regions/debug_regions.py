
import codecs
import json
import os

from PIL import Image, ImageDraw
from collections import OrderedDict
from ast import literal_eval as make_tuple

from celery import Celery
from celery.utils.log import get_task_logger

DEBUG_IMAGE = '../../_TestData/Microsoft_computer-vision-api/bgbill12/bgbill12.png'
DEBUG_REGIONS = '../../_TestData/Microsoft_computer-vision-api/bgbill12/bgbill12.json'

DEBUG_OUTPUT_FOLDER = '_Output'

logger = get_task_logger(__name__)
app = Celery('debug_regions', broker='pyamqp://guest@localhost//')

def _calc_rect(rect_string):
        rect = make_tuple(rect_string)
        rect_list = list(rect)
        rect_list[2] += rect_list[0]
        rect_list[3] += rect_list[1]
        return tuple(rect_list)

@app.task(name='workers.debug_regions.debug_regions', queue='debug_regions')
def debug_regions(*args, **kwargs):

    img = Image.open(os.path.expanduser(DEBUG_IMAGE))
    draw = ImageDraw.Draw(img)

    regions = json.load(codecs.open(os.path.expanduser(DEBUG_REGIONS),
                                    'r', 'utf-8-sig'),
                                    object_pairs_hook=OrderedDict)

    for region in regions['regions']:
        rect = _calc_rect(region['boundingBox'])
        draw.rectangle(rect, outline='red')

        for line in region['lines']:
            rect = _calc_rect(line['boundingBox'])
            draw.rectangle(rect, outline='green')

            for word in line['words']:
                rect = _calc_rect(word['boundingBox'])
                draw.rectangle(rect, outline='blue')

    # Save
    if not os.path.exists(DEBUG_OUTPUT_FOLDER):
        os.makedirs(DEBUG_OUTPUT_FOLDER)

    output_filepath = os.path.join(DEBUG_OUTPUT_FOLDER, 'debug_regions.png')
    # img.save(output_filepath)

    # Show
    # img.show()

    return (args, kwargs)

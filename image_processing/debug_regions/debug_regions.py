#!/usr/bin/env python

import codecs
import json
import os

from PIL import Image, ImageDraw
from collections import OrderedDict
from ast import literal_eval as make_tuple

RABBIT_CONFIG = None
LOGFILE = None

DEBUG_IMAGE = '../_TestData/Microsoft_computer-vision-api/bgbill12/bgbill12.png'
DEBUG_REGIONS = '../_TestData/Microsoft_computer-vision-api/bgbill12/bgbill12.json'

DEBUG_OUTPUT_FOLDER = '_Output'

class DebugRegions(object):

    def __init__(cls, rabbit_config=None, logfile=None):
        # super(DebugRegions, cls).__init__(rabbit_config, logfile)
        pass

    def _calc_rect(cls, rect_string):
        rect = make_tuple(rect_string)
        rect_list = list(rect)
        rect_list[2] += rect_list[0]
        rect_list[3] += rect_list[1]
        return tuple(rect_list)

    def on_request(cls, ch, method, props, body):
        img = Image.open(DEBUG_IMAGE)
        draw = ImageDraw.Draw(img)

        regions = json.load(codecs.open(DEBUG_REGIONS, 'r', 'utf-8-sig'),
                                        object_pairs_hook=OrderedDict)

        for region in regions['regions']:
            rect = cls._calc_rect(region['boundingBox'])
            draw.rectangle(rect, outline='red')

            for line in region['lines']:
                rect = cls._calc_rect(line['boundingBox'])
                draw.rectangle(rect, outline='green')

                for word in line['words']:
                    rect = cls._calc_rect(word['boundingBox'])
                    draw.rectangle(rect, outline='blue')

        # Save
        if not os.path.exists(DEBUG_OUTPUT_FOLDER):
            os.makedirs(DEBUG_OUTPUT_FOLDER)

        output_filepath = os.path.join(DEBUG_OUTPUT_FOLDER, 'debug_regions.png')
        img.save(output_filepath)

        # Show
        img.show()

    # Remove
    def run(cls):
        cls.on_request(None, None, None, None)

    # Remove
    def stop(cls):
        # raise NotImplementedError()
        pass

def main():
    ocr_rpc_orker = DebugRegions(RABBIT_CONFIG, LOGFILE)

    try:
        ocr_rpc_orker.run()
    except KeyboardInterrupt:
        ocr_rpc_orker.stop()

if __name__ == '__main__':
    main()

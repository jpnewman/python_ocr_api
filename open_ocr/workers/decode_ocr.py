#!/usr/bin/env python

import json
import sys

sys.path.append('..')
from rpc_server_base import RpcServer
from rpc_server_base import LOGGER

RABBIT_CONFIG = {
  'AmqpURI':      'amqp://admin:Phaish9ohbaidei6oole@localhost:5672/',
  'Exchange':     'open-ocr-exchange',
  'ExchangeType': 'direct',
  'QueueName':    'decode-ocr',
  'RoutingKey':   'decode-ocr',
  'Reliable':     True
}

LOGFILE = 'decode_ocr.log'

class OcrRpcWorker(RpcServer):

    def __init__(cls, rabbit_config, logfile=None):
        super(OcrRpcWorker, cls).__init__(rabbit_config, logfile)

    def on_request(cls, ch, method, props, body):
        LOGGER.info("Handling request...")
        cls._request_info(ch, method, props, body)

        response = 'decode-ocr\n'
        json_data = json.loads(body)
        for k,v in json_data.items():
            if k != 'img_bytes':
                response += "{0} : {1}\n".format(k, v)
            else:
                response += "{0} : {1}\n".format(k, len(v))

        cls.response_text(ch, method, props, response)


def main():
    ocr_rpc_orker = OcrRpcWorker(RABBIT_CONFIG, LOGFILE)

    try:
        ocr_rpc_orker.run()
    except KeyboardInterrupt:
        ocr_rpc_orker.stop()

if __name__ == '__main__':
    main()

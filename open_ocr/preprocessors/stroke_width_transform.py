#!/usr/bin/env python

import pika
import json
import sys

sys.path.append('..')
from rpc_server_base import RpcServer
from rpc_server_base import LOGGER

RABBIT_CONFIG = {
  'AmqpURI':      'amqp://admin:Phaish9ohbaidei6oole@localhost:5672/',
  'Exchange':     'open-ocr-exchange',
  'ExchangeType': 'direct',
  'QueueName':    'stroke-width-transform',
  'RoutingKey':   'stroke-width-transform',
  'Reliable':     True
}

LOGFILE = 'stroke_width_transform.log'

class Preprocessor(RpcServer):

    def __init__(cls, rabbit_config, logfile=None):
        super(Preprocessor, cls).__init__(rabbit_config, logfile)

    def on_request(cls, ch, method, props, body):
        LOGGER.info("Handling request...")
        cls._request_info(ch, method, props, body)

        # response = 'stroke-width-transform\n'
        # cls.response_text(ch, method, props, response)

        json_data = json.loads(body)
        json_data['img_bytes'] = ''

        basic_properties = pika.BasicProperties(content_type='application/json',
                                                delivery_mode=props.delivery_mode,
                                                correlation_id=props.correlation_id)

        ch.basic_publish(exchange='', # Default Exchange
                         routing_key=props.reply_to,
                         properties=basic_properties,
                         body=str(json_data))
        ch.basic_ack(delivery_tag = method.delivery_tag)


def main():
    ocr_rpc_orker = Preprocessor(RABBIT_CONFIG, LOGFILE)

    try:
        ocr_rpc_orker.run()
    except KeyboardInterrupt:
        ocr_rpc_orker.stop()

if __name__ == '__main__':
    main()

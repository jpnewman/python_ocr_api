
import logging
import pika

LOGGER = logging.getLogger(__name__)


class RpcServer(object):

    def __init__(cls, rabbit_config, logfile=None):
        cls.rabbit_config = rabbit_config
        cls.logfile = logfile

    def _setup_logging(cls):
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        if cls.logfile:
            file_hdlr = logging.FileHandler(cls.logfile)
            file_hdlr.setFormatter(formatter)
            LOGGER.addHandler(file_hdlr)
            LOGGER.setLevel(logging.DEBUG)

        console_hdlr = logging.StreamHandler()
        console_hdlr.setFormatter(formatter)
        LOGGER.addHandler(console_hdlr)
        console_hdlr.setLevel(logging.INFO)

    def _setup_rabbitmq(cls):
        parameters = pika.URLParameters(cls.rabbit_config['AmqpURI'])
        connection = pika.BlockingConnection(parameters)

        channel = connection.channel()

        channel.exchange_declare(exchange=cls.rabbit_config['Exchange'],
                                 exchange_type=cls.rabbit_config['ExchangeType'],
                                 durable=cls.rabbit_config['Reliable'],
                                 auto_delete=False,
                                 internal=False,
                                 arguments=None)

        channel.queue_declare(queue=cls.rabbit_config['QueueName'],
                              durable=True)

        channel.queue_bind(queue=cls.rabbit_config['QueueName'],
                           exchange=cls.rabbit_config['Exchange'],
                           routing_key=cls.rabbit_config['RoutingKey'])

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(cls.on_request, queue=cls.rabbit_config['QueueName'])

        LOGGER.info(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    def _request_info(cls, ch, method, props, body):
        LOGGER.debug("Channel: {0!r}".format(ch))
        LOGGER.debug("Method: {0!r}".format(method))
        LOGGER.debug("Properties: {0!r}".format(props))
        LOGGER.debug("Properties: {0!r}".format(body))

    def response_text(cls, ch, method, props, response):
        basic_properties = pika.BasicProperties(content_type='text/plain',
                                                delivery_mode=props.delivery_mode,
                                                correlation_id=props.correlation_id)

        ch.basic_publish(exchange='', # Default Exchange
                         routing_key=props.reply_to,
                         properties=basic_properties,
                         body=str(response))
        ch.basic_ack(delivery_tag = method.delivery_tag)

    def run(cls):
        cls._setup_logging()
        cls._setup_rabbitmq()

    def stop(cls):
        # raise NotImplementedError()
        pass

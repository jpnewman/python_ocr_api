# Celery configuration file
BROKER_URL = 'pyamqp://guest@localhost//'
CELERY_RESULT_BACKEND = 'amqp://'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = 'Europe/London'
CELERY_ENABLE_UTC = True

CELERY_CREATE_MISSING_QUEUES = True

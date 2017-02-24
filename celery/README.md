
# Celery

## RabbitMQ

~~~
rabbitmq-server
~~~

## Run

~~~
python run.py
~~~

## Worker

|Worker|Description|
|---|---|
|```workers/find_regions```|Find Regions|
|```workers/debug_regions```|Debug Regions|
|```workers/mcs_ocr```|Microsoft OCR|
|```workers/validate_address```|Validate Address|

### Run

> find_regions

~~~
cd workers/find_regions

celery -A find_regions worker --loglevel=info -Q find_regions -n find_regions_01@%h
~~~

> debug_regions

~~~
cd workers/debug_regions

celery -A debug_regions worker --loglevel=info -Q debug_regions -n debug_regions_01@%h
~~~

> mcs_ocr

~~~
cd workers/mcs_ocr

celery -A mcs_ocr worker --loglevel=info -Q mcs_ocr -n mcs_ocr_01@%h
~~~

> validate_address

~~~
cd workers/validate_address

celery -A validate_address worker --loglevel=info -Q validate_address -n validate_address_01@%h
~~~


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

celery -A find_regions worker --loglevel=info -Q find_regions
~~~

> debug_regions

~~~
cd workers/debug_regions

celery -A debug_regions worker --loglevel=info -Q debug_regions
~~~

> validate_address

~~~
cd workers/mcs_ocr

celery -A mcs_ocr worker --loglevel=info -Q mcs_ocr
~~~

> validate_address

~~~
cd workers/validate_address

celery -A validate_address worker --loglevel=info -Q validate_address
~~~

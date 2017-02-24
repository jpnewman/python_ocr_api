
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
|```workers/validate_address```|Validate Address|

### Run

> find_regions

~~~
cd workers/find_regions

celery -A find_regions worker --loglevel=info
~~~

> debug_regions

~~~
cd workers/debug_regions

celery -A debug_regions worker --loglevel=info
~~~

> validate_address

~~~
cd workers/validate_address

celery -A validate_address worker --loglevel=info
~~~


# Open-OCR

This folder contains open-ocr <https://github.com/tleyden/open-ocr> preprocessors and workers written in Python and is currently just a proof of concept. 

## References

- <https://github.com/tleyden/open-ocr>
- <https://github.com/tleyden/open-ocr-client>

## Run

~~~
docker-compose up -d rabbitmq
~~~

~~~
cd workers
chmod u+x ./decode_ocr.py

./decode_ocr.py
~~~

~~~
popd cli-httpd

go run main.go -amqp_uri amqp://admin:Phaish9ohbaidei6oole@127.0.0.1/ -http_port 9292
~~~

## Stop

~~~
docker-compose kill
~~~

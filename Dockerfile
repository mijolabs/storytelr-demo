FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY run.sh /code/run.sh
RUN chmod +x /code/run.sh

COPY ./storytelr.ini /code/storytelr.ini

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN apt-get update && apt-get install -y redis-server

COPY ./app /code/app

CMD /code/run.sh

FROM python:3.10.0-slim

RUN [ "addgroup", "--gid", "1001", "--system", "app", "&&", \
      "adduser", "--no-create-home", "--shell", "/bin/false", \
      "--disabled-password", "--uid", "1001", "--system", "--group", "app" ]

USER app
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./whisper.ini /code/whisper.ini

RUN [ "pip", "install", "--no-cache-dir", "--upgrade", "-r", "/code/requirements.txt" ]

RUN [ "apt-get", "update", "&&", "apt-get", "install", "-y", "redis-server" ]

COPY ./app /code/app

RUN [ "/usr/bin/redis-server", "--daemonize", "yes", "--requirepass", "whisper-demo" ]
ENTRYPOINT [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port" ]
CMD [ "8000" ]

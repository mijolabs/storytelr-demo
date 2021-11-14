#!/usr/bin/env bash

/usr/bin/redis-server --daemonize yes --requirepass storytelr-demo

cd /code
uvicorn app.main:app --host 0.0.0.0 --port 8000

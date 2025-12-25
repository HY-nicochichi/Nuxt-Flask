#!/bin/bash

cd flaskapi
python3 core.py
exec gunicorn core:app \
  --bind 0.0.0.0:5000 \
  --worker-class gevent \
  --workers 8 \
  --access-logfile -

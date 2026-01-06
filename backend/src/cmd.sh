cd flaskapi
python3 core.py
exec gunicorn core:app \
  --bind 0.0.0.0:8000 \
  --worker-tmp-dir /dev/shm \
  --worker-class gevent \
  --workers 8 \
  --access-logfile - \
  --error-logfile -

sleep 7

pytest tests
gunicorn core:app -b :5000 -k gevent -w 8

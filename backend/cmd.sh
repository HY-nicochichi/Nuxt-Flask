pytest tests/jwt.py tests/user.py
python3 core.py
gunicorn core:app -b 0.0.0.0:5000 -k gevent -w 8 --access-logfile -

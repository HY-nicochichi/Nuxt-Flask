from os import environ
from json import dumps

wsgi_app: str = 'src:app'
bind: str = f'0.0.0.0:{environ['PORT']}'
control_socket_disable: bool = True
worker_tmp_dir: str = '/dev/shm'
worker_class: str = 'gthread'
workers: int = 1
threads: int = int(environ['APP_CONCURRENCY'])
timeout: int = 0
graceful_timeout: int = 5
keep_alive: int = 630
max_requests: int = 3000
max_requests_jitter: int = 500
errorlog: str = '-'
accesslog: str = '-'
access_log_format: str = dumps({
    'timestamp': '%(t)s',
    'client_ip': '%(h)s',
    'method': '%(m)s',
    'path': '%(U)s',
    'query': '%(q)s',
    'referer': '%(f)s',
    'user_agent': '%(a)s',
    'status_code': '%(s)s',
    'body_bytes': '%(b)s',
    'process_sec': '%(L)s'
})
forwarded_allow_ips: str = '*'

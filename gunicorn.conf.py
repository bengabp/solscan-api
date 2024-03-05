# Gunicorn configuration file

import multiprocessing
from src.config import logs_dir
import os

# max_requests = 1000
# max_requests_jitter = 50

accesslog = os.path.join(logs_dir, "gunicorn_access.log")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

bind = "0.0.0.0:8080"

worker_class = "uvicorn.workers.UvicornWorker"
workers = 4
worker_memory_limit = 1000 * 1024 * 1024  # 1000 MB in bytes
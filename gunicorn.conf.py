# Gunicorn configuration file

import multiprocessing
from src.config import logs_dir
import os

max_requests = 1000
max_requests_jitter = 50

accesslog = os.path.join(logs_dir, "gunicorn_access.log")
access_log_format = '[%(asctime)s] [PID %(process)d] [%(threadName)s] [%(name)s] [%(levelname)s] %(message)s'

bind = "0.0.0.0:8080"

worker_class = "uvicorn.workers.UvicornWorker"
workers = (multiprocessing.cpu_count() * 2) + 1

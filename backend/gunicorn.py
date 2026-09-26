import os
from multiprocessing import cpu_count

is_debug = os.getenv("DEBUG") == "True"

def get_workers():
    if is_debug:
        return 1
    return cpu_count() * 2 + 1

bind = '0.0.0.0:8000'
worker_class = 'gthread'
workers = get_workers()
threads = 2
max_requests = 1000
preload_app = not is_debug
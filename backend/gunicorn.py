from multiprocessing import cpu_count

def get_workers():
    return cpu_count() * 2 + 1

bind = '0.0.0.0:8000'
worker_class = 'gthread'
workers = get_workers()
threads = 2
max_requests = 1000
preload_app = True
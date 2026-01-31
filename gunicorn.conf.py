# Gunicorn configuration file
import multiprocessing

# Worker class
worker_class = 'uvicorn.workers.UvicornWorker'

# Worker processes
workers = 2  # Adjust based on available resources

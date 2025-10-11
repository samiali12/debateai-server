import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_USERNAME = os.getenv("REDIS_USERNAME")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

redis_url = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"

celery_app = Celery(
    "worker",
    broker=redis_url,
    backend=redis_url,
)


celery_app.conf.task_routes = {"app.tasks.*": {"queue": "emails"}}
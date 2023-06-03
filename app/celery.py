from celery import Celery
from kombu.utils.url import safequote
from app import config

settings = config.get_settings()

broker_url = "sqs://{aws_access_key}:{aws_secret_key}@".format(
    aws_access_key=safequote(settings.aws_access_key_id),
    aws_secret_key=safequote(settings.aws_secret_access_key),
)

celery_app = Celery(
    "glaza_workers",
    broker_url=broker_url,
    result_backend=None,
    task_default_queue="event-documentation-updates.fifo",
    include=["app.background_tasks"],
    broker_transport_options={
        "predefined_queues": {
            "event-documentation-updates.fifo": {
                "url": "https://sqs.us-east-1.amazonaws.com/862411997490/event-documentation-updates.fifo",
                "access_key_id": settings.aws_access_key_id,
                "secret_access_key": settings.aws_secret_access_key,
            }
        }
    },
)

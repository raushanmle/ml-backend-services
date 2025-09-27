from celery_app import celery_app
from app.app import run


@celery_app.task(
    name="tasks.run_celery",
    queue="tasks.run_celery-queue",
    bind=True
)
def run_task(self, val: str):
    run(val)
    return "Task completed with value: %s" % val
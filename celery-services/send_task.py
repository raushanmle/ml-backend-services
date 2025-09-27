import sys
 
sys.path.append(".")
from celery_app import celery_app as celery
 

celery.send_task(
    "tasks.run_celery",
    args=("aa",),
    queue="tasks.run_celery-queue",
)
from celery import Celery

celery_app = Celery(__name__, include=["tasks"])  # auto-import tasks module
celery_app.config_from_object("celery_config")

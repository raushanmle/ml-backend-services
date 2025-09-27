import os

from dotenv import load_dotenv

load_dotenv()

broker_url = "amqp://{user}:{password}@{rabbitmq_host}:{rabbitmq_port}//".format(
    user=os.environ.get("RABBITMQ_USER", "guest"),
    password=os.environ.get("RABBITMQ_PASSWORD", "guest"),
    rabbitmq_host=os.environ.get("RABBITMQ_HOST", "localhost"),
    rabbitmq_port=os.environ.get("RABBITMQ_PORT", 5672),
)
result_backend = "redis://{redis_host}:{redis_port}/0".format(
    redis_host=os.environ.get("REDIS_HOST", "localhost"),
    redis_port=os.environ.get("REDIS_PORT", 6379),
)

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]

# enable_utc = True

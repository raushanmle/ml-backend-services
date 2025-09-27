#!/bin/bash

set -o errexit
set -o nounset

celery -A celery_app:celery_app worker -l INFO -Q tasks.run_celery,tasks.run_celery-queue -c 1 --prefetch-multiplier 1

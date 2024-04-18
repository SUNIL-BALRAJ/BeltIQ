# celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab  # Import crontab for scheduling

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Schedule your task to run every 2 minutes
app.conf.beat_schedule = {
    'update-json-file': {
        'task': 'core.cloud.read_data_from_azure_storage',  # Update with the correct task name
        'schedule': crontab(minute='*/2'),  # Run every 2 minutes
    },
}

# Optionally configure timezone (for example, 'UTC')
app.conf.timezone = 'UTC'

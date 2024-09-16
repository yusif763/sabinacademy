from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab  # Import crontab for periodic tasks

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sabinadmin.settings')

app = Celery('sabinadmin')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Add periodic tasks to the Celery beat schedule
app.conf.beat_schedule = {
    'update-next-payments-everyday': {
        'task': 'core.tasks.update_next_payments',
        'schedule': crontab(hour=0, minute=0),  # Runs every day at midnight
    },
    'update-daily-payments-everyday': {
        'task': 'core.tasks.update_daily_payments',
        'schedule': crontab(hour=0, minute=0),  # Runs every day at midnight
    },
    'send-next-payments-report-everyday': {
        'task': 'core.tasks.send_next_payments_report',
        'schedule': crontab(hour=8, minute=0),  # Send report at 8 AM
    },
}

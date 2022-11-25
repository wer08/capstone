import os
from celery import Celery
from celery.schedules import crontab




# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final_project.settings')

app = Celery('final_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

import django
django.setup()

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

from fitness.tasks import set_calories_to_zero

app.conf.beat_schedule = {
    'set-everyday': {
        'task': 'fitness.tasks.set_calories_to_zero',
        'schedule': crontab(hour=0, minute=0)
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


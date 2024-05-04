import os

# celery imports
from celery import Celery
from celery.schedules import crontab

# task imports
from loans.services.tasks import fetch_and_update_industries_trends_task, test_task


# default settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LoanApprovalBackend.settings')

# create celery app
app = Celery('LoanApprovalBackend')

# load celery config from settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# discover tasks in all apps
app.autodiscover_tasks()

# run tasks periodically
app.conf.beat_schedule = {
    'fetch-industry-trends': {
        'task': 'fetch_and_update_industries_trends_task',
        'schedule': crontab(day_of_week="6"),
    },
    'test-task': {
        'task': 'test_task',
        'schedule': 50.0,
    }
}

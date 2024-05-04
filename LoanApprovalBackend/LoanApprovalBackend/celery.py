import os
import django

# celery imports
from celery import Celery
from celery.schedules import crontab

# default settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LoanApprovalBackend.settings')
django.setup()

# create celery app
app = Celery('LoanApprovalBackend')

app.conf.task_modules = (
    "loans.services.tasks.test_task",
    "loans.services.tasks.fetch_and_update_industries_trends_task"
)

# load celery config from settings
app.config_from_object('django.conf:settings', namespace='CELERY')


# run tasks periodically
app.conf.beat_schedule = {
    'fetch-industry-trends': {
        'task': 'loans.services.tasks.fetch_and_update_industries_trends_task',
        'schedule': crontab(day_of_week='6', hour='9', minute='45'),
    },
    'test-task': {
        'task': 'loans.services.tasks.test_task',
        'schedule': 5.0,
    }
}

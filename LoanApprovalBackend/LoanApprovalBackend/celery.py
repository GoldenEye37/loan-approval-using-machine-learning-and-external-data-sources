import os

from celery import Celery

# config celery


# default settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LoanApprovalBackend.settings')

# create celery app
app = Celery('LoanApprovalBackend')

# load celery config from settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# discover tasks in all apps
app.autodiscover_tasks()

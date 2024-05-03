# make sure app is imported when Django starts
# so that the task is registered

from .celery import app as celery_app

__all__ = ('celery_app',)
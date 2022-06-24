from __future__ import absolute_import
import os   
from celery import Celery

from celery.schedules import crontab

os.environ.setdeafault('DJANGO_SETTINGS_MODULE','djangoWebScraper.settings')

app = Celery('djangoWebScraper')

app.conf.timezone = "UTC"
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
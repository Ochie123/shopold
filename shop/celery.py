import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')

#app = Celery('shop', broker='amqp://guest:**@localhost:5672//')

app = Celery('shop', broker='pyamqp://shop:shop546=re@localhost:5672//')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')

<<<<<<< HEAD
=======
#app = Celery('shop', broker='amqp://guest:**@localhost:5672//')
>>>>>>> 309766bdf0e7bfa8ea615d7bf18962f3fa438035
app = Celery('shop', broker='pyamqp://shop:shop546=re@localhost:5672//')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

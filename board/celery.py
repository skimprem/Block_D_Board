import os
from celery import Celery
from celery.schedules import crontab
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'board.settings')
 
app = Celery('board')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete_codes_every_minute': {
        'task': 'sign.tasks.codes_delete',
        'schedule': crontab(),
    },
    'notification_every_moday_8am': {
        'task': 'adverts.tasks.week_notification',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    }
}
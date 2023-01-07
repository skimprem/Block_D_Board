from celery import shared_task
from sign.models import OneTimeCode
from datetime import datetime, timedelta

@shared_task
def codes_delete():
    old_codes = OneTimeCode.objects.all().exclude(time_in__gt = datetime.now() - timedelta(minutes = 3))
    old_codes.delete()
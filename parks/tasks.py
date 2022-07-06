from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.utils import timezone

from main.models import WeekSchedule


@shared_task
def refresh_schedules():
    schedules = WeekSchedule.objects.filter(arquived=False)
    for schedule in schedules:
        if schedule.deadline.end_date <= timezone.now().date():
            schedule.arquived = True
            schedule.save()

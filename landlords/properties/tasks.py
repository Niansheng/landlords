from __future__ import absolute_import, unicode_literals
from celery import shared_task

from properties.notify_landlord import notify_landlord


@shared_task
def notify():
    notify_landlord()

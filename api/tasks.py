from __future__ import absolute_import

from celery import shared_task
from api.elasticsearchModel import elastic

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)
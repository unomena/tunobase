'''
CORE APP

Celery tasks

'''
from celery.decorators import task

from tunobase.core import models


@task(ignore_result=True)
def publish_objects():
    models.Version.objects.publish_objects()

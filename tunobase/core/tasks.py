'''
Created on 21 Oct 2013

@author: michael
'''
from celery.decorators import task

from tunobase.core import models

@task(ignore_result=True)
def publish_objects():
    models.ContentModel.objects.permitted().publish_objects()
'''
Created on 21 Oct 2013

@author: michael
'''
from celery.decorators import task

from tunobase.commenting import models

@task(ignore_result=True)
def remove_flagged_comments():
    models.CommentModel.objects.remove_flagged_comments()
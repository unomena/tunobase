"""
Commenting App

This module provides an interface to Celery tasks for removing
flagged comments.

Classes:
    n/a

Functions:
    remove_flagged_comments

Created on 21 Oct 2013

@author: michael

"""
from celery.decorators import task

from tunobase.commenting import models


@task(ignore_result=True)
def remove_flagged_comments():
    """Delete flagged comments."""

    models.CommentModel.objects.remove_flagged_comments()

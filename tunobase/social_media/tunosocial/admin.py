"""
TUNOSOCIAL APP

This module describes how the tunosocial app integrates into
Django's admin.

Created on 28 Oct 2013

@author: michael

"""
from django.contrib import admin

from tunobase.social_media.tunosocial import models

admin.site.register(models.Like)

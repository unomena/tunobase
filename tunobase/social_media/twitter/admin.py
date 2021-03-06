"""
TWITTER APP

This module describes how the twitter module is displayed
in Django's admin.

Created on 28 Oct 2013

@author: michael

"""
from django.contrib import admin

from tunobase.social_media.twitter import models

admin.site.register(models.TwitterUser)

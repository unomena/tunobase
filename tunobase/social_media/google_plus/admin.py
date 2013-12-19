"""
GOOGLE PLUS APP

This module describes how the google_plus model appears
in Django's admin.

Created on 28 Oct 2013

@author: michael

"""
from django.contrib import admin
 
from tunobase.social_media.google_plus import models
 
admin.site.register(models.GooglePlusUser)

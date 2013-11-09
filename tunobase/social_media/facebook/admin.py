'''
Created on 28 Oct 2013

@author: michael
'''
from django.contrib import admin

from tunobase.social_media.facebook import models

admin.site.register(models.FacebookUser)
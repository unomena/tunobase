'''
Created on 28 Oct 2013

@author: michael
'''
from django.contrib import admin

from tunobase.tagging import models

admin.site.register(models.Tag)
admin.site.register(models.ContentObjectTag)
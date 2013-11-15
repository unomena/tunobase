'''
Created on 22 Oct 2013

@author: michael
'''
from django.contrib import admin

from tunobase.bulk_loading import models

admin.site.register(models.BulkUploadImage)
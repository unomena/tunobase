'''
Created on 23 Oct 2013

@author: michael
'''
from django.contrib import admin

from tunobase.api import models

class RequestAdmin(admin.ModelAdmin):
    list_display = (
            'service', 'status', 'created_timestamp', 'completed_timestamp',
    )
    list_filter = (
            'service', 'status', 'created_timestamp', 'completed_timestamp',
    )

admin.site.register(models.Destination)
admin.site.register(models.Service)
admin.site.register(models.Request, RequestAdmin)

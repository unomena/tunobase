'''
Created on 23 Oct 2013

@author: michael
'''
from django.contrib import admin

from tunobase.corporate.media import models

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'venue_name', 'venue_address', 'start', 'end')
    list_filter = ('title', 'venue_name', 'venue_address', 'start', 'end')
    search_fields = ('title', 'venue_name', 'venue_address')

admin.site.register(models.Event, EventAdmin)
admin.site.register(models.PressRelease)
admin.site.register(models.MediaCoverage)
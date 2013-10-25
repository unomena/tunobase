'''
Created on 23 Oct 2013

@author: michael
'''
from django.contrib import admin

from tunobase.corporate.media import models

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'state', 'venue_name', 'venue_address', 'start', 'end')
    list_filter = ('title', 'state', 'venue_name', 'venue_address', 'start', 'end')
    search_fields = ('title', 'venue_name', 'venue_address')
    
class PressReleaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'state', 'created_at', 'publish_at')
    list_filter = ('title', 'state', 'created_at', 'publish_at')
    search_fields = ('title',)
    
class MediaCoverageAdmin(admin.ModelAdmin):
    list_display = ('title', 'state', 'created_at', 'publish_at')
    list_filter = ('title', 'state', 'created_at', 'publish_at')
    search_fields = ('title',)

admin.site.register(models.Event, EventAdmin)
admin.site.register(models.PressRelease, PressReleaseAdmin)
admin.site.register(models.MediaCoverage, MediaCoverageAdmin)
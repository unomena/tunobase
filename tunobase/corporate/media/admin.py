"""
MEDIA APP

This module provides the Django admin layout for the media model.

Classes:
    EventAdmin
    ArticleAdmin
    PressReleaseAdmin
    MediaCoverageAdmin

Functions:
    n/a

Created on 23 Oct 2013

@author: michael

"""
from django.contrib import admin

from tunobase.corporate.media import models

class EventAdmin(admin.ModelAdmin):
    """Display events in Django admin."""

    list_display = (
            'title', 'slug', 'state', 'venue_name', 'venue_address', 'start',
            'end'
    )
    list_filter = (
            'title', 'state', 'venue_name', 'venue_address', 'start', 'end'
    )
    search_fields = ('title', 'venue_name', 'venue_address')

class ArticleAdmin(admin.ModelAdmin):
    """Display articles in Django admin."""

    list_display = ('title', 'slug', 'state', 'created_at', 'publish_at')
    list_filter = ('title', 'state', 'created_at', 'publish_at')
    search_fields = ('title',)

class PressReleaseAdmin(admin.ModelAdmin):
    """Display press releases in Django admin."""

    list_display = ('title', 'slug', 'state', 'created_at', 'publish_at')
    list_filter = ('title', 'state', 'created_at', 'publish_at')
    search_fields = ('title',)

class MediaCoverageAdmin(admin.ModelAdmin):
    """Display media in Django admin."""

    list_display = ('title', 'slug', 'state', 'created_at', 'publish_at')
    list_filter = ('title', 'state', 'created_at', 'publish_at')
    search_fields = ('title',)

admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.PressRelease, PressReleaseAdmin)
admin.site.register(models.MediaCoverage, MediaCoverageAdmin)

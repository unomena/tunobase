"""
TAGGING APP

This module describes how the taggin app is displayed in
Django's admin.

Classes:
    TagAdmin

Functions:
    n/a

Created on 28 Oct 2013

@author: michael

"""
from django.contrib import admin

from tunobase.tagging import models

class TagAdmin(admin.ModelAdmin):
    """Display the tag model in the admin."""
    list_display = ('title', 'description', 'site')
    list_filter = ('title', 'site')
    search_fields = ('title', 'site')

admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.ContentObjectTag)

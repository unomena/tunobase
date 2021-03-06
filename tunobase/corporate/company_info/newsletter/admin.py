"""
NEWSLETTER APP

This module details how the newsletter models are displayed
in Django's admin.

Classes:
    ContactMessageAdmin

Function:
    n/a

Created on 23 Oct 2013

@author: michael

"""
from django.contrib import admin

from tunobase.corporate.company_info.newsletter import models

class ContactMessageAdmin(admin.ModelAdmin):
    """How to display models in the admin."""

    list_display = ('name', 'email', 'user', 'site', 'timestamp')
    list_filter = ('name', 'email', 'user', 'site', 'timestamp')
    search_fields = ('name', 'email','timestamp')

admin.site.register(models.Newsletter)
admin.site.register(models.NewsletterRecipient)
admin.site.register(models.RichNewsletterPart)
admin.site.register(models.PlainNewsletterPart)

"""
CONTACT APP

This module contains diplay information for the models in the
Django admin.

Classes:
    ContactMessageAdmin

Functions:
    n/a

Created on 23 Oct 2013

@author: michael

"""
from django.contrib import admin

from tunobase.corporate.company_info.contact import models

class ContactMessageAdmin(admin.ModelAdmin):
    """Determine how to display fields in the Django admin."""
    list_display = ('name', 'email', 'user', 'site', 'timestamp')
    list_filter = ('name', 'email', 'user', 'site', 'timestamp')
    search_fields = ('name', 'email','timestamp')

admin.site.register(models.ContactMessage, ContactMessageAdmin)

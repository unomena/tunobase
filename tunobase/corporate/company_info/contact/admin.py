'''
Created on 23 Oct 2013

@author: michael
'''
from django.contrib import admin

from tunobase.corporate.company_info.contact import models

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'user', 'site', 'timestamp')
    list_filter = ('name', 'email', 'user', 'site', 'timestamp')
    search_fields = ('name', 'email','timestamp')

admin.site.register(models.ContactMessage, ContactMessageAdmin)
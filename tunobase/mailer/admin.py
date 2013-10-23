'''
Created on 22 Oct 2013

@author: michael
'''
from django.contrib import admin

from tunobase.mailer import models

class OutboundEmailAdmin(admin.ModelAdmin):
    list_display = ('user', 'to_addresses', 'bcc_addresses', 'sent_timestamp', 'subject')
    list_filter = ('user', 'to_addresses', 'bcc_addresses', 'sent_timestamp', 'subject')
    search_fields = ('user__email', 'to_addresses', 'bcc_addresses', 'subject')

admin.site.register(models.OutboundEmail, OutboundEmailAdmin)
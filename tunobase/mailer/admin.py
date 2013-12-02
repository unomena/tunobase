'''
Created on 22 Oct 2013

@author: michael
'''
from django.contrib import admin

from tunobase.mailer import models

class OutboundEmailAdmin(admin.ModelAdmin):
    list_display = ('user', 'to_addresses', 'bcc_addresses', 'sent_timestamp', 'subject', 'site')
    list_filter = ('user', 'to_addresses', 'bcc_addresses', 'sent_timestamp', 'subject', 'site')
    search_fields = ('user__email', 'to_addresses', 'bcc_addresses', 'subject', 'site')

admin.site.register(models.OutboundEmail, OutboundEmailAdmin)
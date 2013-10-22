'''
Created on 22 Oct 2013

@author: michael
'''
from django.contrib import admin

from tunobase.mailer import models

class OutboundEmailAdmin(admin.ModelAdmin):
    list_display = ('user', 'sent_timestamp', 'subject')
    list_filter = ('user', 'sent_timestamp', 'subject')
    search_fields = ('user__email', 'subject')

admin.site.register(models.OutboundEmail, OutboundEmailAdmin)
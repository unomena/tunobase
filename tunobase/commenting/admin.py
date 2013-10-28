'''
Created on 28 Oct 2013

@author: michael
'''
from django.contrib import admin

from tunobase.commenting import models

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'visible_to', 'in_reply_to', 'moderated_by', 'moderated_on')
    list_filter = ('user',)
    search_fields = ('comment',) 

admin.site.register(models.CommentModel, CommentModelAdmin)
admin.site.register(models.CommentFlag)
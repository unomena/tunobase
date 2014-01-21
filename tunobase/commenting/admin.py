"""
Commenting App

This module determines how the comment model is displayed
in Django's admin.

"""
from django.contrib import admin

from tunobase.commenting import models


class CommentModelAdmin(admin.ModelAdmin):
    """How to display the comment model in Django's admin."""

    list_display = (
            'user', 'comment', 'in_reply_to', 'moderated_by', 'moderated_at'
    )
    list_filter = ('user',)
    search_fields = ('comment',)

admin.site.register(models.CommentModel, CommentModelAdmin)
admin.site.register(models.CommentFlag)

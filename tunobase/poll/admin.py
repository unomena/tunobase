"""
POLL APP

This module describes how the poll model displays in
Django's admin.

Classes:
    PollAnswerInline
    PollQuestionAdmin

Functions:
    n/a

Created on 26 Mar 2013

@author: michael

"""
from django.contrib import admin

from tunobase.poll import models

class PollAnswerInline(admin.TabularInline):
    """Display PollAnswer model."""

    model = models.PollAnswer


class PollQuestionAdmin(admin.ModelAdmin):
    """Display PollAnswerInline with PollAnswer model."""

    inlines = [PollAnswerInline]

admin.site.register(models.PollQuestion, PollQuestionAdmin)
admin.site.register(models.PollAnswer)

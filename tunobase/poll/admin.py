'''
Created on 26 Mar 2013

@author: michael
'''
from django.contrib import admin

from tunobase.poll import models

class PollAnswerInline(admin.TabularInline):
    model = models.PollAnswer

class PollQuestionAdmin(admin.ModelAdmin):
    inlines = [PollAnswerInline]

admin.site.register(models.PollQuestion, PollQuestionAdmin)
admin.site.register(models.PollAnswer)
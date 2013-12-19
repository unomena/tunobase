"""
EULA APP

This module describes how the EULA model gets displayed
in Django's admin.

Classes:
    EULAVersionInline
    EULAAdmin

Functions:
    n/a

"""
from django.contrib import admin

from tunobase.eula import models

class EULAVersionInline(admin.TabularInline):
    model = models.EULAVersion

class EULAAdmin(admin.ModelAdmin):
    inlines = [EULAVersionInline,]

admin.site.register(models.EULA)
admin.site.register(models.EULAVersion)
admin.site.register(models.UserEULA)

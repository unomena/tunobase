"""
CATEGORIES APP

This module describes how the categories app is displayed in
Django's admin.

"""
from django.contrib import admin

from tunobase.categories import models

class CategoryAdmin(admin.ModelAdmin):
    """Display the category model in the admin."""
    list_display = ('title', 'description', 'site')
    list_filter = ('title', 'site')
    search_fields = ('title', 'site')

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.ContentObjectCategory)

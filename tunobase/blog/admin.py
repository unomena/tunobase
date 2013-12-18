"""
BLOG APP

This module determines how to display the Blog app in Django's admin
and lists other model functions.

Classes:
    BlogEntryAdmin

Functions:
    n/a

Created on 22 Oct 2013

@author: michael

"""
from django.contrib import admin

from tunobase.blog import models

class BlogEntryAdmin(admin.ModelAdmin):
    """
    This class determines how to display the blog app in Django's admin.

    """
    list_display = (
            'title', 'state', 'publish_at', 'author_list', 'authors_alternate'
    )
    list_filter = ('title', 'state', 'publish_at')
    search_fields = ('title',)

    def author_list(self, model):
        """Return a comma separate list of the authors."""

        return ', '.join(
                [user.display_name for user in model.author_users.all()]
        )

admin.site.register(models.Blog)
admin.site.register(models.BlogEntry, BlogEntryAdmin)

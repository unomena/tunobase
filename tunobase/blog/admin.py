'''
Created on 22 Oct 2013

@author: michael
'''
from django.contrib import admin

from tunobase.blog import models

class BlogEntryAdmin(admin.ModelAdmin):
    list_display = (
            'title', 'state', 'publish_at', 'author_list', 'authors_alternate'
    )
    list_filter = ('title', 'state', 'publish_at')
    search_fields = ('title',)

    def author_list(self, model):
        return ', '.join(
                [user.display_name for user in model.author_users.all()]
        )

admin.site.register(models.Blog)
admin.site.register(models.BlogEntry, BlogEntryAdmin)

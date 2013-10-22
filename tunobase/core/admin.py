'''
Created on 22 Oct 2013

@author: michael
'''
from django.contrib import admin

from tunobase.core import models

class ContentModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'site_list')
    list_filter = ('title', 'created_at')
    search_fields = ('title',)
    
    def site_list(self, model):
        return ', '.join([site.domain for site in model.sites.all()])

admin.site.register(models.ContentModel, ContentModelAdmin)
admin.site.register(models.DefaultImage)
admin.site.register(models.ImageBanner)
admin.site.register(models.HTMLBanner)
admin.site.register(models.ImageBannerSet)
admin.site.register(models.HTMLBannerSet)
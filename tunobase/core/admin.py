"""
CORE APP

This module determines the way the core app displays in
Django's admin.

"""
from django.contrib import admin

from tunobase.core import models

class SiteListAdminMixin(object):
    """Return a list of sites."""

    def site_list(self, model):
        """Return a comma separated list of sites."""

        return ', '.join([site.domain for site in model.sites.all()])

class ContentModelAdmin(admin.ModelAdmin, SiteListAdminMixin):
    """Determine how the content model is displayed in the admin."""

    list_display = (
            'title', 'state', 'slug', 'created_at', 'publish_at', 'site_list'
    )
    list_filter = ('title', 'state', 'created_at', 'publish_at')
    search_fields = ('title',)

class BannerSetAdmin(admin.ModelAdmin, SiteListAdminMixin):
    """Determine how the banner set is displayed in the admin."""

    list_display = ('slug', 'site_list')

class GalleryAdmin(admin.ModelAdmin, SiteListAdminMixin):
    """Determined how the gallery is displayed in the admin."""

    list_display = ('slug', 'site_list')

admin.site.register(models.ContentModel, ContentModelAdmin)
admin.site.register(models.ContentBlock, ContentModelAdmin)
admin.site.register(models.DefaultImage)
admin.site.register(models.ImageBanner)
admin.site.register(models.HTMLBanner)
admin.site.register(models.ImageBannerSet, BannerSetAdmin)
admin.site.register(models.HTMLBannerSet, BannerSetAdmin)
admin.site.register(models.GalleryImage)
admin.site.register(models.Gallery, GalleryAdmin)

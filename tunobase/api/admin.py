'''
API App

'''
from django.contrib import admin

from tunobase.api import models


class RequestAdmin(admin.ModelAdmin):
    """
    This class determines how the api app should be displayed in
    the Django admin.

    """
    list_display = (
            'service', 'status', 'created_timestamp', 'completed_timestamp',
    )
    list_filter = (
            'service', 'status', 'created_timestamp', 'completed_timestamp',
    )

admin.site.register(models.Destination)
admin.site.register(models.Service)
admin.site.register(models.Request, RequestAdmin)

"""
Bulk Loading App

This module registers the BulkUploadImage and BulkUploadData models
in Django's admin.

"""
from django.contrib import admin

from tunobase.bulk_loading import models

admin.site.register(models.BulkUploadImage)
admin.site.register(models.BulkUploadData)

"""
Bulk Loading App

This module provides generic django URL routing.

"""
from django.conf.urls import patterns, url

from tunobase.bulk_loading import views, forms

urlpatterns = patterns('',
    url(r'^bulk-image-upload/$',
        views.BulkImageUpload.as_view(
            form_class=forms.BulkImageUploadForm,
        ),
        name='bulk_loading_bulk_image_upload'
    ),
)

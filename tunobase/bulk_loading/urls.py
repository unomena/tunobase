'''
Created on 25 Oct 2013

@author: michael
'''
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

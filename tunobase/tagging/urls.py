"""
TAGGING APP

This module provides generic django URL routing.

Created on 25 Oct 2013

@author: michael

"""
from django.conf.urls import patterns, url

from tunobase.tagging import views, forms

urlpatterns = patterns('', 
    url(r'^retrieve-tags/$',
        views.RetrieveTags.as_view(),
        name='retrieve_tags'
    ),

    url(r'^update-tags/$',
        views.UpdateTags.as_view(
            form_class=forms.TagUpdateForm
        ),
        name='update_tags'
    ),
)

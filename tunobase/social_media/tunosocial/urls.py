"""
TUNOSOCIAL APP

This module provides generic django URL routing.

Created on 25 Oct 2013

@author: michael

"""
from django.conf.urls import patterns, url

from tunobase.social_media.tunosocial import views

urlpatterns = patterns('',

    url(r'^add-like/$',
        views.AddLike.as_view(),
        name='tunosocial_add_like'
    ),

     url(r'^remove-like/$',
        views.RemoveLike.as_view(),
        name='tunosocial_remove_like'
    ),
)

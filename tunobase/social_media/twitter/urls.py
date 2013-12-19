"""
TWITTER APP

This module provides generic django URL routing.

Created on 25 Oct 2013

@author: michael

"""
from django.conf.urls import patterns, url

from tunobase.social_media.twitter import views, forms

urlpatterns = patterns('',

    url(r'^twitter-pre-login/$',
        views.PreLogin.as_view(),
        name='twitter_pre_login'
    ),

    url(r'^twitter-login-callback/$',
        views.LoginCallback.as_view(),
        name='twitter_login_callback'
    ),

    url(r'^twitter-request-email/$',
        views.RequestEmail.as_view(
            template_name='twitter/request_email.html',
            form_class=forms.RequestEmailForm
        ),
        name='twitter_request_email'
    ),
)

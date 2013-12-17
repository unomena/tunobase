'''
Created on 25 Oct 2013

@author: michael
'''
from django.conf.urls import patterns, url

from tunobase.social_media.google_plus import views

urlpatterns = patterns('',

    url(r'^google-plus-pre-login/$',
        views.PreLogin.as_view(),
        name='google_plus_pre_login'
    ),

    url(r'^google-plus-login-callback/$',
        views.LoginCallback.as_view(),
        name='google_plus_login_callback'
    ),
)

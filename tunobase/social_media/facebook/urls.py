'''
Created on 25 Oct 2013

@author: michael
'''
from django.conf.urls import patterns, url

from tunobase.social_media.facebook import views

urlpatterns = patterns('',
                                          
    url(r'^facebook-login-callback/$',
        views.LoginCallback.as_view(),
        name='facebook_login_callback'
    ),
)

"""
CONSOLE APP

This module provides generic django URL routing.

"""
from django.conf.urls import patterns, url

from tunobase.console import views

urlpatterns = patterns('',

    url(r'^$',
        views.Console.as_view(template_name='console/index.html'),
        name='console'),
)

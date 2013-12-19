"""
POLL APP

This module provides generic django URL routing.

Created on 26 Mar 2013

@author: michael

"""
from django.conf.urls import patterns, url

from tunobase.poll import views, forms

urlpatterns = patterns('',

    url(r'^answer/(?P<pk>\d+)/$',
        views.PollAnswer.as_view(
            form_class=forms.PollAnswerForm,
            ajax_template_name='poll/includes/poll_results.html',
            template_name='poll/poll_results.html'
        ),
        name='poll_answer'),

    url(r'^results/(?P<pk>\d+)/$',
        views.PollResults.as_view(
            template_name='poll/poll_results.html'
        ),
        name='poll_results'),
)

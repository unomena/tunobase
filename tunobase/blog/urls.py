"""
Blog App

This module provides generic django URL routing.

"""
from django.conf.urls import patterns, url

from tunobase.blog import views

urlpatterns = patterns('',
    url(r'^list/$',
        views.BlogList.as_view(
            template_name='blog/blog_list.html'
        ),
        name='blog_list'
    ),

    url(r'^detail/(?P<slug>[\w-]+)/$',
        views.BlogEntryDetail.as_view(
            template_name='blog/blog_entry_detail.html'
        ),
        name='blog_entry_detail'
    ),

    url(r'^(?P<slug>[\w-]+)/$',
        views.BlogDetail.as_view(
            paginate_by=10,
            template_name='blog/blog_detail.html',
            partial_template_name='blog/includes/blog_entries.html'
        ),
        name='blog_detail'
    ),

    (r'^feed/$', views.BlogFeed()),
)

"""
MEDIA APP

This module provides generic django URL routing.

Created on 23 Oct 2013

@author: michael

"""
from django.conf.urls import patterns, url

from tunobase.corporate.media import views

urlpatterns = patterns('',

    url(r'^articles/$',
        views.Articles.as_view(
            template_name='media/articles/articles.html',
            paginate_by=20
        ),
        name='media_articles'
    ),

    url(r'^article/(?P<slug>[-\w]+)/$',
        views.ArticleDetail.as_view(
            template_name='media/articles/article_detail.html',
        ),
        name='media_article_detail'
    ),

    url(r'^media-coverage/$',
        views.MediaCoverage.as_view(
            template_name='media/media_coverage/media_coverage.html',
            paginate_by=20
        ),
        name='media_media_coverage'
    ),

    url(r'^events/$',
        views.Events.as_view(
            template_name='media/events/events.html',
        ),
        name='media_events'
    ),

    url(r'^press-releases/$',
        views.PressReleases.as_view(
            template_name='media/press_releases/press_releases.html',
            paginate_by=20
        ),
        name='media_press_releases'
    ),

    url(r'^press-release/(?P<slug>[-\w]+)/$',
        views.PressReleaseDetail.as_view(
            template_name='media/press_releases/press_release_detail.html',
        ),
        name='media_press_release_detail'
    ),
)

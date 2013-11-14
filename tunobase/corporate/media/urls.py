'''
Created on 23 Oct 2013

@author: michael
'''
from django.conf.urls import patterns, url
from django.views import generic as generic_views

from tunobase.corporate.media import views

urlpatterns = patterns('',

    url(r'^articles/$',
        views.Articles.as_view(
            template_name='media/articles/articles.html',
            paginate_by=20
        ),
        name='media_articles'
    ),
                       
    url(r'^press-releases/$',
        views.PressReleases.as_view(
            template_name='media/press_releases/press_releases.html',
            paginate_by=20
        ),
        name='media_press_releases'
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
)
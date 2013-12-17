'''
Created on 05 Mar 2013

@author: michael
'''
from django.conf.urls import patterns, url

from tunobase.corporate.media.console import views, forms

urlpatterns = patterns('',
    url(r'^media-coverage/create/$',
        views.MediaCoverageCreate.as_view(
            form_class=forms.MediaCoverageForm,
            template_name=\
                    'console/media/media_coverage/media_coverage_edit.html'
        ),
        name='console_media_media_coverage_create'
    ),

    url(r'^media-coverage/update/(?P<pk>\d+)/$',
        views.MediaCoverageUpdate.as_view(
            form_class=forms.MediaCoverageForm,
            template_name=\
                    'console/media/media_coverage/media_coverage_edit.html'
        ),
        name='console_media_media_coverage_update'
    ),

    url(r'^media-coverage/(?P<pk>\d+)/detail/$',
        views.MediaCoverageDetail.as_view(
            template_name=\
                    'console/media/media_coverage/media_coverage_detail.html'
        ),
        name='console_media_media_coverage_detail'
    ),

    url(r'^media-coverage/delete/(?P<pk>\d+)/$',
        views.MediaCoverageDelete.as_view(),
        name='console_media_media_coverage_delete'
    ),

    url(r'^media-coverage/list/$',
        views.MediaCoverageList.as_view(
            template_name=\
                    'console/media/media_coverage/media_coverage_list.html',
            paginate_by=20
        ),
        name='console_media_media_coverage_list'
    ),
)

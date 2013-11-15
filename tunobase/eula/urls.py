'''
Created on 06 Mar 2013

@author: michael
'''
from django.conf.urls import patterns, url

from tunobase.eula import forms, views

urlpatterns = patterns('',         
    url(r'^sign/$',
        views.SignEULA.as_view(
            template_name='eula/sign_eula.html',
            form_class=forms.SignEULAForm
        ),
        name='eula_sign'
    ),
                       
    url(r'^sign/(?P<content_type_id>\d+)/(?P<object_pk>\d+)/$',
        views.SignEULAObject.as_view(
            template_name='eula/sign_eula_object.html',
            form_class=forms.SignEULAForm
        ),
        name='eula_sign'
    ),
)
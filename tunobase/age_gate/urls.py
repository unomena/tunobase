'''
Created on 05 Mar 2013

@author: michael
'''
from django.conf.urls import patterns, url
from django.conf import settings

from tunobase.age_gate import views, forms

urlpatterns = patterns('',

    url(r'^$',
        views.AgeGate.as_view(
            form_class=forms.AgeGateForm,
            template_name='age_gate/age_gate_form.html'
        ),
        name='age_gate'
    ),
)
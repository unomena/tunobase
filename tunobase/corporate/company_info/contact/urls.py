'''
Created on 23 Oct 2013

@author: michael
'''
from django.conf.urls import patterns, url
from django.views import generic as generic_views

from honeypot.decorators import check_honeypot

from tunobase.corporate.company_info.contact import views, forms

urlpatterns = patterns('',

    url(r'^contact/$',
        check_honeypot(views.Contact.as_view(
            template_name='contact/contact.html',
            form_class=forms.ContactMessageForm
        )),
        name='company_info_contact'
    ),
                       
    url(r'^contact/thanks/$',
        generic_views.TemplateView.as_view(
            template_name='contact/contact_thanks.html'
        ),
        name='company_info_contact_thanks'
    ),
)
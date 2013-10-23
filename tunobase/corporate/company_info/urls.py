from django.conf.urls.defaults import patterns, url
from django.views import generic as generic_views

from tunobase.corporate.company_info import views, forms

urlpatterns = patterns('',

    url(r'^contact/$',
        views.Contact.as_view(
            template_name='company_info/contact.html',
            form_class=forms.ContactMessageForm
        ),
        name='company_info_contact'
    ),
                       
    url(r'^contact/thanks/$',
        generic_views.TemplateView.as_view(
            template_name='company_info/contact_thanks.html'
        ),
        name='company_info_contact_thanks'
    ),
)
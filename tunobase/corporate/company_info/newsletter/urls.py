from django.conf.urls import patterns, url
from django.views import generic as generic_views

from tunobase.corporate.company_info.newsletter import views, forms

urlpatterns = patterns('',
    url(r'^secure/subscribe/$',
        views.NewsletterSubscribe.as_view(
            form_class=forms.NewsletterSubscribeForm
        ),
        name='newsletter_subscribe'
    ),
    
    url(r'^secure/unsubscribe/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.NewsletterUnsubscribe.as_view(
            template_name='newsletter/unsubscribe.html',
        ),
        name='newsletter_unsubscribe'
    ),
                       
    url(r'^secure/email/validate/$',
        views.EmailValidate.as_view(),
        name='newsletter_email_validate'),
)
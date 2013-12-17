'''
Created on 23 Oct 2013

@author: michael
'''
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.http import base36_to_int
from django.views import generic as generic_views

from tunobase.core import utils as core_utils
from tunobase.corporate.company_info.newsletter import models, utils

class NewsletterSubscribe(generic_views.CreateView):

    def form_valid(self, form):
        obj = form.save(self.request)

        return core_utils.respond_with_json({
            'success': True,
            'message': 'You have been successfully \
                    subscribed to our newsletter'
        })


class NewsletterUnsubscribe(generic_views.TemplateView):

    def get(self, request, *args, **kwargs):
        try:
            uid_int = base36_to_int(self.kwargs['uidb36'])
            newsletter_recipient = models.NewsletterRecipient\
                    .active_recipients.get(pk=uid_int)
        except (ValueError, OverflowError,
                models.NewsletterRecipient.DoesNotExist):
            newsletter_recipient = None

        if newsletter_recipient is not None and \
           utils.token_generator.check_token(
                   newsletter_recipient, self.kwargs['token']
            ):
            newsletter_recipient.unsubscribe()
            return self.render_to_response(
                self.get_context_data()
            )

        return redirect('index')


class EmailValidate(generic_views.View):

    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')
        User = get_user_model()

        if User.objects.filter(email__iexact=email).exists() or \
           models.NewsletterRecipient.objects\
           .filter(email__iexact=email)\
           .exists():
            return HttpResponse('false')

        return HttpResponse('true')

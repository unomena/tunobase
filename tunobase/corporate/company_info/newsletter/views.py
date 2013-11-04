'''
Created on 23 Oct 2013

@author: michael
'''
from django.views import generic as generic_views
from django.utils.http import base36_to_int
from django.shortcuts import redirect

from tunobase.corporate.company_info.newsletter import models, utils

class NewsletterUnsubscribe(generic_views.TemplateView):
    
    def get(self, request, *args, **kwargs):
        try:
            uid_int = base36_to_int(self.kwargs['uidb36'])
            newsletter_recipient = models.NewsletterRecipient.active_recipients.get(pk=uid_int)
        except (ValueError, OverflowError, models.NewsletterRecipient.DoesNotExist):
            newsletter_recipient = None
            
        if newsletter_recipient is not None and \
           utils.token_generator.check_token(newsletter_recipient, self.kwargs['token']):
            newsletter_recipient.unsubscribe()
            return self.render_to_response(
                self.get_context_data()
            )
        
        return redirect('index')
        
        
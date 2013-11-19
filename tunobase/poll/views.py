'''
Created on 05 Mar 2013

@author: michael
'''
from django.views import generic as generic_views
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext

from tunobase.core import utils as core_utils
from tunobase.poll import models

class PollAnswer(generic_views.FormView):
    '''
    View for handling poll submissions
    '''
    def get_form_kwargs(self):
        kwargs = super(PollAnswer, self).get_form_kwargs()
        
        self.poll = core_utils.get_permitted_object_or_404(
            models.PollQuestion, pk=self.kwargs['pk']
        )
        kwargs['poll'] = self.poll
        
        return kwargs
    
    def form_valid(self, form):
        cookie_name = 'poll_%s_voted' % self.kwargs['pk']
        poll_voted = self.request.COOKIES.get(cookie_name, False)
        if not poll_voted:
            messages.error(self.request, 'You have already voted in this poll.')
        else:
            form.save()
            messages.success(self.request, 'You have voted.')
        
        response = core_utils.respond_with_json({
            'success': True,
            'results': render_to_string(
                self.template_name, RequestContext(self.request, {
                    'results': self.poll.answers.get_poll_percentages()
                })
            )
        })
        response.set_cookie(cookie_name, True)
        
        return response
        
    def form_invalid(self, form):
        return core_utils.respond_with_json({
            'success': False,
            'reason': str(form.errors)
        })
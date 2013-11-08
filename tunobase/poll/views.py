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
from tunobase.poll import utils, models

class PollAnswer(generic_views.FormView):
    '''
    View for handling poll submissions
    '''
    def get_form_kwargs(self):
        self.poll = get_object_or_404(models.PollQuestion, pk=self.kwargs['pk'])
        kwargs = super(PollAnswer, self).get_form_kwargs()
        kwargs['poll'] = self.poll
        return kwargs
    
    def form_valid(self, form):
        poll_voted = self.request.session.get('poll_voted', False)
        
        if not poll_voted:
            self.request.session['poll_voted'] = True
            answers = form.save()
            messages.success(self.request, 'You have voted.')
        else:
            messages.error(self.request, 'You have already voted in this poll.')
            
        return core_utils.respond_with_json({
            'success': True,
            'results': render_to_string(
                self.template_name, RequestContext(self.request, {
                    'results': utils.get_poll_percentages(
                        self.poll.answers.all()
                    )
                })
            )
        })
        
    def form_invalid(self, form):
        return core_utils.respond_with_json({
            'success': False,
            'reason': str(form.errors)
        })
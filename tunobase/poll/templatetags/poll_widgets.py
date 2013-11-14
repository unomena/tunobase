'''
Created on 26 Mar 2013

@author: michael
'''
from copy import copy

from django import template
from django.core.exceptions import ImproperlyConfigured

try:
    from preferences import preferences
except ImportError:
    preferences = None

from tunobase.poll import forms, utils, models

register = template.Library()

@register.inclusion_tag('poll/inclusion_tags/poll_widget.html', takes_context=True)
def poll_widget(context, pk=None):
    context = copy(context)
    if pk is None:
        if preferences is None:
            raise ImproperlyConfigured(
                "No pk specified. Please add the preferences app to your settings.py"
                " file to load a default poll"
            )
            
        poll = preferences.SitePreferences.active_poll
    else:
        try:
            poll = models.PollQuestion.permitted.for_current_site().get(pk=pk)
            print poll
        except models.PollQuestion.DoesNotExist:
            context.update({
                'error': True,
                'pk': pk
            })
            return context
    
    context.update({
        'form': forms.PollAnswerForm(poll=poll),
        'results': utils.get_poll_percentages(poll.permitted_answers),
    })
    return context

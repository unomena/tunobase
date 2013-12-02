'''
Created on 31 Oct 2013

@author: michael
'''
from copy import copy

from django import template

register = template.Library()

@register.inclusion_tag('social_media/inclusion_tags/social_media_share_widget.html', takes_context=True)
def social_media_share_widget(context, *args, **kwargs):
    context = copy(context)
    context['theme'] = kwargs.pop('theme', 'basic')
    for arg in args:
        context[arg] = True
    return context
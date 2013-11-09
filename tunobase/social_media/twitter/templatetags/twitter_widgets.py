'''
Created on 08 Nov 2013

@author: michael
'''
from copy import copy

from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse_lazy

import facebook

register = template.Library()

@register.inclusion_tag('twitter/inclusion_tags/twitter_login_widget.html', takes_context=True)
def twitter_login_widget(context):
    context = copy(context)
    
    context.update({
        'auth_url': reverse_lazy('twitter_pre_login')
    })
    
    return context
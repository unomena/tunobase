'''
Created on 08 Nov 2013

@author: michael
'''
from copy import copy

from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse_lazy
from django.utils.http import quote

register = template.Library()

@register.inclusion_tag('google_plus/inclusion_tags/google_plus_login_widget.html', takes_context=True)
def google_plus_login_widget(context, login_button_text='Login with Google'):
    from tunobase.social_media.google_plus import utils
    context = copy(context)
    context.update({
        'auth_url': quote(utils.FLOW.step1_get_authorize_url()),
        'login_button_text': login_button_text
    })
    
    return context
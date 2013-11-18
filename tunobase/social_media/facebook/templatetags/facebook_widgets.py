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

import facebook

register = template.Library()

@register.inclusion_tag('facebook/inclusion_tags/facebook_login_widget.html', takes_context=True)
def facebook_login_widget(context, perms=None, login_button_text='Login with Facebook'):
    context = copy(context)
    login_redirect_uri = 'http://%s%s' % (
        Site.objects.get_current().domain, 
        reverse_lazy('facebook_login_callback')
    )
    csrf_token = unicode(context['csrf_token'])
    context['request'].session['facebook_state'] = csrf_token
    
    if perms:
        perms = ['email'] + perms.split(',')
    else:
        perms = ['email']
    
    context.update({
        'auth_url': quote(facebook.auth_url(
            settings.FACEBOOK_APP_ID, 
            login_redirect_uri,
            perms,
            csrf_token
        )),
        'login_button_text': login_button_text
    })
    
    return context
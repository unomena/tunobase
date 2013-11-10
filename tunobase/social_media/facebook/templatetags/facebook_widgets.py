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

@register.inclusion_tag('facebook/inclusion_tags/facebook_login_widget.html', takes_context=True)
def facebook_login_widget(context):
    context = copy(context)
    login_redirect_uri = 'http://%s%s' % (
        Site.objects.get_current().domain, 
        reverse_lazy('facebook_login_callback')
    )
    csrf_token = unicode(context['csrf_token'])
    context['request'].session['facebook_state'] = csrf_token
    context.update({
        'auth_url': facebook.auth_url(settings.FACEBOOK_APP_ID, login_redirect_uri, ['email'], csrf_token)
    })
    
    return context
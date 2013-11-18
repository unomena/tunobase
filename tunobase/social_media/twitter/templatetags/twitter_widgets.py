'''
Created on 08 Nov 2013

@author: michael
'''
from copy import copy

from django import template

register = template.Library()

@register.inclusion_tag('twitter/inclusion_tags/twitter_login_widget.html', takes_context=True)
def twitter_login_widget(context, login_button_text='Login with Twitter'):
    context = copy(context)
    
    context.update({
        'login_button_text': login_button_text
    })
    
    return context
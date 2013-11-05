'''
Created on 29 Oct 2013

@author: michael
'''
from copy import copy

from django import template
from django.contrib.contenttypes.models import ContentType

from tunobase.corporate.company_info.newsletter import forms

register = template.Library()

@register.inclusion_tag('newsletter/inclusion_tags/newsletter_widget.html', takes_context=True)
def newsletter_widget(context):
    context = copy(context)
    form = forms.NewsletterSubscribeForm()
        
    context.update({
        'form': form,
    })
    
    return context
'''
Created on 29 Oct 2013

@author: michael
'''
from copy import copy

from django import template
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from tunobase.commenting import models

register = template.Library()

@register.inclusion_tag('commenting/inclusion_tags/commenting_widget.html', takes_context=True)
def commenting_widget(context, obj):
    context = copy(context)
    site = Site.objects.get_current()
    queryset = models.CommentModel.permitted.get_comments_for_object(
        obj,
        site
    )
        
    context.update({
        'object': obj,
        'content_type_id': ContentType.objects.get_for_model(obj).id,
        'comments': queryset
    })
    
    return context
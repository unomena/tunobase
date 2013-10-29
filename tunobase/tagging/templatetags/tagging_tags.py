'''
Created on 29 Oct 2013

@author: michael
'''
from django import template
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from tunobase.tagging import models

register = template.Library()

@register.inclusion_tag('tagging/inclusion_tags/tags_widget.html', takes_context=True)
def tags_widget(context, obj):
    site = Site.objects.get_current()
    queryset = models.ContentObjectTag.objects.get_tags_for_object(obj, site)
    
    tags = [{'title': obj.tag.title} for obj in queryset]

    if context['user'].is_authenticated() and context['user'].is_staff:
        tags.append({'title': '+'})
        
    return {
        'object': obj,
        'content_type_id': ContentType.objects.get_for_model(obj).id,
        'tags': tags
    }
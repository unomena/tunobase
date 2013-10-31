'''
Created on 29 Oct 2013

@author: michael
'''
from copy import copy

from django import template
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from tunobase.tagging import models

register = template.Library()

@register.inclusion_tag('tagging/inclusion_tags/tags_widget.html', takes_context=True)
def tags_widget(context, obj):
    context = copy(context)
    site = Site.objects.get_current()
    queryset = models.ContentObjectTag.objects.get_tags_for_object(obj, site)
    
    tags = [{'title': tag_obj.tag.title} for tag_obj in queryset]
        
    context.update({
        'object': obj,
        'content_type_id': ContentType.objects.get_for_model(obj).id,
        'tags': tags
    })
    
    return context

@register.inclusion_tag('tagging/inclusion_tags/tag_cloud_widget.html', takes_context=True)
def tag_cloud_widget(context, app_label, model):
    context = copy(context)
    site = Site.objects.get_current()
    queryset = models.ContentObjectTag.objects.get_unique_tags_for_object_type(
        app_label, 
        model, 
        site
    )
    
    tags = [{'title': tag_obj.title} for tag_obj in queryset]
        
    context.update({
        'tags': tags
    })
    
    return context
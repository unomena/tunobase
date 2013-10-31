'''
Created on 31 Oct 2013

@author: michael
'''
from django import template

from tunobase.core import models

register = template.Library()

@register.inclusion_tag('tunobase/inclusion_tags/content_block.html', takes_context=True)
def content_block(context, slug):
    try:
        content = models.ContentBlock.permitted.get(slug=slug)
    except  models.ContentBlock.DoesNotExist:
        content = None
    
    return {
        'content': content,
        'user': context['request'].user,
        'slug': slug
    }
    
@register.inclusion_tag('tunobase/inclusion_tags/image_bannerset.html')
def image_bannerset(slug):
    try:
        bannerset = models.ImageBannerSet.permitted.get(slug=slug)
    except  models.ImageBannerSet.DoesNotExist:
        bannerset = None
    
    return {
        'bannerset': bannerset,
        'slug': slug
    }

@register.inclusion_tag('tunobase/inclusion_tags/html_bannerset.html')
def html_bannerset(slug):
    try:
        bannerset = models.HTMLBannerSet.permitted.get(slug=slug)
    except  models.HTMLBannerSet.DoesNotExist:
        bannerset = None
    
    return {
        'bannerset': bannerset,
        'slug': slug
    }
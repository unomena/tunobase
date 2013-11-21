'''
Created on 29 Oct 2013

@author: michael
'''
from django import template
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from tunobase.core import models, nodes

register = template.Library()

@register.tag
def smart_query_string(parser, token):
    '''
    Outputs current GET query string with additions appended.
    Additions are provided in token pairs.
    '''
    args = token.split_contents()
    additions = args[1:]

    addition_pairs = []
    while additions:
        addition_pairs.append(additions[0:2])
        additions = additions[2:]

    return nodes.SmartQueryStringNode(addition_pairs)

@register.assignment_tag
def gallery_surrounding_image_pks(gallery, gallery_image_pk):
    gallery_images = list(gallery.images.all())
    previous_image_pk = None
    next_image_pk = None
    for i, gallery_image in enumerate(gallery_images):
        if gallery_image.pk == gallery_image_pk:
            try:
                previous_image_pk = gallery_images[i+1].pk
            except IndexError:
                pass
            
            try:
                next_image_pk = gallery_images[i-1].pk
            except IndexError:
                pass
            
            break
            
    return {
        'next_image_pk': next_image_pk,
        'previous_image_pk': previous_image_pk
    }
    
@register.filter
def letterify(value):
    return str(unichr(65 + value))

@register.filter
def class_name(obj):
    return obj.__class__.__name__
'''
Created on 08 Nov 2013

@author: michael
'''
from copy import copy

from django import template
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from tunobase.social_media.tunosocial import models

register = template.Library()

@register.inclusion_tag('tunosocial/inclusion_tags/tunosocial_likes_widget.html', takes_context=True)
def tunosocial_likes_widget(context, obj):
    context = copy(context)
    site = Site.objects.get_current()
    num_likes = models.Like.objects.get_num_likes_for_object(obj, site)
    already_liked = models.Like.objects.get_already_liked(context['user'], obj, site)
        
    context.update({
        'object': obj,
        'content_type_id': ContentType.objects.get_for_model(obj).id,
        'num_likes': num_likes,
        'already_liked': already_liked
    })
    
    return context
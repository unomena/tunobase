'''
Created on 19 Nov 2013

@author: michael
'''
from django import template
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from tunobase.social_media.tunosocial import models

register = template.Library()

@register.inclusion_tag('tunosocial/inclusion_tags/num_likes.html')
def num_likes(obj):
    site = Site.objects.get_current()
    num_likes = models.Like.objects.get_num_likes_for_object(obj, site)
    
    return {
        'num_likes': num_likes
    }
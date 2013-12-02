'''
Created on 19 Nov 2013

@author: michael
'''
from django import template
from django.contrib.contenttypes.models import ContentType

from tunobase.commenting import models

register = template.Library()

@register.inclusion_tag('commenting/inclusion_tags/num_comments.html')
def num_comments(obj):
    content_type_id= ContentType.objects.get_for_model(obj).id
    num_comments = models.CommentModel.objects.permitted().get_comments_for_object(
        content_type_id, 
        obj.pk
    ).count()
    
    return {
        'num_comments': num_comments
    }
'''
Created on 29 Oct 2013

@author: michael
'''
from copy import copy

from django import template
from django.contrib.contenttypes.models import ContentType

from tunobase.commenting import models, forms

register = template.Library()

@register.inclusion_tag('commenting/inclusion_tags/commenting_widget.html', takes_context=True)
def commenting_widget(context, obj, paginate_by=1):
    context = copy(context)
    content_type_id= ContentType.objects.get_for_model(obj).id
    comments_form = forms.LoadCommentsForm({
        'paginate_by': paginate_by,
        'page': 1,
        'comment_content_type_id': content_type_id,
        'comment_object_pk': obj.pk,
    })
    
    if comments_form.is_valid():
        comments, total_comments = comments_form.retrieve()
    else:
        comments, total_comments = None, 0
        
    context.update({
        'paginate_by': paginate_by,
        'object': obj,
        'object_pk': obj.pk,
        'content_type_id': content_type_id,
        'comments': comments,
        'total_comments': total_comments
    })
    
    return context
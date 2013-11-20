'''
Created on 29 Oct 2013

@author: michael
'''
from copy import copy
import urllib

from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse_lazy

from tunobase.commenting import models

register = template.Library()

@register.inclusion_tag('commenting/inclusion_tags/commenting_widget.html', 
                        takes_context=True)
def commenting_widget(context, obj, paginate_by=10, page_obj=None):
    context = copy(context)
    content_type_id= ContentType.objects.get_for_model(obj).id
    if page_obj is None:
        comments = models.CommentModel.objects.permitted().get_comments_for_object(
            content_type_id, 
            obj.pk
        )
        paginator = Paginator(comments, paginate_by)
        page = paginator.page(1)
    else:
        page = page_obj
    params = urllib.urlencode({
        'content_type_id': content_type_id, 
        'object_pk': obj.pk,
        'paginate_by': paginate_by
    })
        
    context.update({
        'content_type_id': content_type_id,
        'object': obj,
        'object_list': page,
        'page_obj': page,
        'load_more_url': '%s?%s' % (reverse_lazy('load_more_comments'), params)
    })
    
    return context
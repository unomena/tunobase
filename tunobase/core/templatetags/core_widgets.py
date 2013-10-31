'''
Created on 31 Oct 2013

@author: michael
'''
from copy import copy

from django import template
from django.template.defaulttags import url

from tunobase.core import models, nodes

register = template.Library()

@register.inclusion_tag('core/inclusion_tags/pagination_widget.html', takes_context=True)
def pagination_widget(context, page_obj):
    context = copy(context)
    context.update({
        'page_obj': page_obj,
        'paginator': getattr(page_obj, 'paginator', None),
    })
    return context

@register.inclusion_tag('core/inclusion_tags/ajax_more_pagination_widget.html', takes_context=True)
def ajax_more_pagination_widget(context, page_obj, load_more_url):
    context = copy(context)
    context.update({
        'load_more_url': load_more_url,
        'page_obj': page_obj,
        'paginator': getattr(page_obj, 'paginator', None),
    })
    return context

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
    
@register.tag
def breadcrumb_widget(parser, token):
    '''
    Renders the breadcrumb.
    
    Examples:
        {% breadcrumb "Title of breadcrumb" url_var %}
        {% breadcrumb context_var  url_var %}
        {% breadcrumb "Just the title" %}
        {% breadcrumb just_context_var %}
    '''
    return nodes.BreadcrumbNode(token.split_contents()[1:])


@register.tag
def breadcrumb_url_widget(parser, token):
    '''
    Same as breadcrumb
    but instead of url context variable takes in all the
    arguments URL tag takes.
    
    Examples:
        {% breadcrumb "Title of breadcrumb" person_detail person.id %}
        {% breadcrumb person.name person_detail person.id %}
    '''
    bits = token.split_contents()
    if len(bits)==2:
        return breadcrumb_widget(parser, token)

    # Extract our extra title parameter
    title = bits.pop(1)
    token.contents = ' '.join(bits)

    url_node = url(parser, token)

    return nodes.UrlBreadcrumbNode(title, url_node)
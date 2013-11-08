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

@register.inclusion_tag('core/inclusion_tags/content_block_widget.html', takes_context=True)
def content_block_widget(context, slug):
    context = copy(context)
    try:
        content = models.ContentBlock.permitted.for_current_site().get(slug=slug)
    except models.ContentBlock.DoesNotExist:
        content = None
    
    context.update({
        'content': content,
        'slug': slug
    })
    
    return context

@register.inclusion_tag('core/inclusion_tags/gallery_widget.html', takes_context=True)
def gallery_widget(context, slug):
    context = copy(context)
    try:
        gallery = models.Gallery.permitted.for_current_site().get(slug=slug)
    except models.Gallery.DoesNotExist:
        gallery = None
    
    context.update({
        'gallery': gallery,
        'slug': slug
    })
    
    return context
    
@register.inclusion_tag('core/inclusion_tags/image_bannerset_widget.html', takes_context=True)
def image_bannerset_widget(context, slug):
    context = copy(context)
    try:
        bannerset = models.ImageBannerSet.permitted.for_current_site().get(slug=slug)
    except models.ImageBannerSet.DoesNotExist:
        bannerset = None
    
    context.update({
        'bannerset': bannerset,
        'slug': slug
    })
    
    return context

@register.inclusion_tag('core/inclusion_tags/html_bannerset_widget.html', takes_context=True)
def html_bannerset_widget(context, slug):
    context = copy(context)
    try:
        bannerset = models.HTMLBannerSet.permitted.for_current_site().get(slug=slug)
    except models.HTMLBannerSet.DoesNotExist:
        bannerset = None
    
    context.update({
        'bannerset': bannerset,
        'slug': slug
    })
    
    return context
    
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
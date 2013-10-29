'''
Created on 29 Oct 2013

@author: michael
'''
from copy import copy

from django import template
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.template.defaulttags import url

from tunobase.core import nodes

register = template.Library()

@register.tag
def smart_query_string(parser, token):
    """
    Outputs current GET query string with additions appended.
    Additions are provided in token pairs.
    """
    args = token.split_contents()
    additions = args[1:]

    addition_pairs = []
    while additions:
        addition_pairs.append(additions[0:2])
        additions = additions[2:]

    return nodes.SmartQueryStringNode(addition_pairs)

@register.inclusion_tag('core/inclusion_tags/pagination.html', takes_context=True)
def pagination(context, page_obj):
    context = copy(context)
    context.update({
        'page_obj': page_obj,
        'paginator': getattr(page_obj, 'paginator', None),
    })
    return context
    
@register.filter
def letterify(value):
    return str(unichr(65 + value))

@register.tag
def breadcrumb(parser, token):
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
def breadcrumb_url(parser, token):
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
        return breadcrumb(parser, token)

    # Extract our extra title parameter
    title = bits.pop(1)
    token.contents = ' '.join(bits)

    url_node = url(parser, token)

    return nodes.UrlBreadcrumbNode(title, url_node)
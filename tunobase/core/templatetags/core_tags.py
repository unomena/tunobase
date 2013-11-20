'''
Created on 29 Oct 2013

@author: michael
'''
from django import template
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

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
    
@register.filter
def letterify(value):
    return str(unichr(65 + value))

@register.filter
def class_name(obj):
    return obj.__class__.__name__
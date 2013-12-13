'''
Created on 22 Oct 2013

@author: michael
'''
import json
import types

from django import http
from django.template import Context, Template
from django.utils.encoding import smart_unicode

def respond_with_json(response_dict):
    '''
    Convert a Python dictionary to a JSON object and return a Django
    HttpResponse with mimetype application/javascript
    '''
    response = http.HttpResponse(json.dumps(response_dict, indent=4))
    response['mimetype'] = 'application/javascript'
    response['Access-Control-Allow-Origin'] = '*'
    return response

def get_choice_value(choice_display, choices):
    '''
    Lookup a value in a given tuple
    '''
    choices_dict = dict(choices)

    for key in choices_dict.keys():
        if choices_dict[key] == choice_display:
            return key

    return None

def get_client_ip(request):
    '''
    Retrieve the client's IP Address from a given HttpRequest
    '''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_object_for_current_site_or_404(klass, *args, **kwargs):
    '''
    Retrieve an object from a Django model only if
    it is a part of the current Site
    '''
    queryset = klass.objects
    try:
        return queryset.for_current_site().get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise http.Http404(
            'No %s matches the given query.' % queryset\
                    .model._meta.object_name
        )

def get_permitted_object_or_404(klass, *args, **kwargs):
    '''
    Retrieve an object from a Django model only if
    its State is published
    '''
    queryset = klass.objects.permitted()
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise http.Http404(
            'No %s matches the given query.' % queryset\
                    .model._meta.object_name
        )

def get_permitted_object_for_current_site_or_404(klass, *args, **kwargs):
    '''
    Retrieve an object from a Django model only if
    its State is published and it is a part of the 
    current Site
    '''
    queryset = klass.objects.permitted()
    try:
        return queryset.for_current_site().get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise http.Http404(
            'No %s matches the given query.' % queryset\
                    .model._meta.object_name
        )

def create_crumb(title, url=None):
    '''
    Helper function to create breadcrumb HTML
    '''
    crumb = '&raquo;'
    if url:
        crumb = "%s<a href='%s'>%s</a>" % (crumb, url, title)
    else:
        crumb = "%s&nbsp;%s" % (crumb, title)

    return crumb

def render_string_to_string(string, context):
    '''
    Renders a string with context
    '''
    template = Template(string)
    context = Context(context)
    return template.render(context)

def ensure_unicode(the_string):
    '''
    Checking if unicode
    '''
    if not type(the_string) == types.UnicodeType:
    #        the_string = unicode(str(the_string))
        the_string = smart_unicode(the_string)

    return smart_unicode(the_string)

def not_null_str(obj):
    '''
    Ensures that the returned string is not null
    '''
    if obj == None:
        return ''
    else:
        return ensure_unicode(obj)

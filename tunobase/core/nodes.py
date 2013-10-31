'''
Created on 29 Oct 2013

@author: michael
'''
from django.template import loader, Node, Variable
from django.utils.encoding import smart_str, smart_unicode
from django.template import VariableDoesNotExist

from tunobase.core import utils

class BreadcrumbNode(Node):
    def __init__(self, vars):
        '''
        First var is title, second var is url context variable
        '''
        self.vars = map(Variable,vars)

    def render(self, context):
        title = self.vars[0].var

        if title.find("'")==-1 and title.find('"')==-1:
            try:
                val = self.vars[0]
                title = val.resolve(context)
            except:
                title = ''

        else:
            title=title.strip("'").strip('"')
            title=smart_unicode(title)

        url = None

        if len(self.vars)>1:
            val = self.vars[1]
            try:
                url = val.resolve(context)
            except VariableDoesNotExist:
                url = None

        return utils.create_crumb(title, url)

class UrlBreadcrumbNode(Node):
    def __init__(self, title, url_node):
        self.title = Variable(title)
        self.url_node = url_node

    def render(self, context):
        title = self.title.var

        if title.find("'") == -1 and title.find('"') == -1:
            try:
                val = self.title
                title = val.resolve(context)
            except:
                title = ''
        else:
            title=title.strip("'").strip('"')
            title=smart_unicode(title)

        url = self.url_node.render(context)
        return utils.create_crumb(title, url)
    
class SmartQueryStringNode(Node):
    def __init__(self, addition_pairs):
        self.addition_pairs = []
        for key, value in addition_pairs:
            self.addition_pairs.append((Variable(key) if key \
                    else None, Variable(value) if value else None))

    def render(self, context):
        q = dict([(k, v) for k, v in context['request'].GET.items()])
        for key, value in self.addition_pairs:
            if key:
                key = key.resolve(context)
                if value:
                    value = value.resolve(context)
                    q[key] = value
                else:
                    q.pop(key, None)
            qs = '&'.join(['%s=%s' % (k, v) for k, v in q.items()])
        return '?' + qs if len(q) else ''
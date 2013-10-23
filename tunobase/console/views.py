'''
Created on 05 Mar 2013

@author: michael
'''
from django.views import generic as generic_views
from django.shortcuts import get_object_or_404

from tunobase.core import mixins as core_mixins

class AdminMixin(core_mixins.ConsoleUserRequiredMixin):
    raise_exception = False

class Console(AdminMixin, generic_views.TemplateView):
    pass
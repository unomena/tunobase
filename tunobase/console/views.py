"""
CONSOLE APP

This module provides the views for the console.

Classes:
    AdminMixin
    Console

Functions:
    n/a

Created on 05 Mar 2013

@author: michael

"""
from django.views import generic as generic_views

from tunobase.console import mixins

class AdminMixin(mixins.ConsoleUserRequiredMixin):
    """Require console user to log in."""

    raise_exception = False


class Console(AdminMixin, generic_views.TemplateView):
    pass

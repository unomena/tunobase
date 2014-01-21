"""
CONSOLE APP

This module provides the views for the console.

"""
from django.views import generic as generic_views

from tunobase.console import mixins

class AdminMixin(mixins.ConsoleUserRequiredMixin):
    """Require console user to log in."""

    raise_exception = False


class Console(AdminMixin, generic_views.TemplateView):
    pass

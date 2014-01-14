"""
Age Gate App

This module provides dispatch functionality. If the user passes the
age gate requirements, send them on to view the site's content. However,
should they failed the age gate requirements, have the server return a
forbidden response and disallow the user to view the site's content.

Classes:
    AgeGateMixin

Functions:
    n/a

Created on 23 Oct 2013

@author: michael

"""
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.conf import settings

from tunobase.age_gate import utils


class AgeGateMixin(object):
    """Mixin to check if the user is old enough to view the content."""

    age_gate_url = getattr(settings, 'AGE_GATE_URL', 'age_gate')
    raise_exception = False

    def dispatch(self, request, *args, **kwargs):
        """Where should we send the user off to next.

        If raise_exception is set to True, the server will return a
        forbidden response, disallowing the user to access the site's
        content.

        """
        age_gate_passed = request.session.get('age_gate_passed', False)

        if not age_gate_passed:
            if self.raise_exception:
                raise PermissionDenied
            else:
                return utils.redirect_to_age_gate(
                    request.get_full_path(),
                    reverse_lazy(self.age_gate_url)
                )

        return super(AgeGateMixin, self).dispatch(request, *args, **kwargs)

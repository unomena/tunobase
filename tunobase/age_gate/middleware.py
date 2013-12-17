"""
This module provides redirect functionality should the user
successfully pass the age gate requirement.

Clases:
    AgeGateMiddleware

Functions:
    n/a

Created on 08 Nov 2013

@author: michael

"""
from django.core.urlresolvers import reverse_lazy
from django.conf import settings

from tunobase.age_gate import utils

class AgeGateMiddleware(object):
    """
    Enable this Middleware to make the entire site Age-Gated

    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Check if user is above the required age.

        Redirect to age gate template if user is not of required age.

        """
        age_gate_url = getattr(settings, 'AGE_GATE_URL', 'age_gate')

        if not request.resolver_match.url_name == age_gate_url:
            age_gate_passed = request.session.get('age_gate_passed', False)
            if not age_gate_passed:
                return utils.redirect_to_age_gate(
                    request.get_full_path(), 
                    reverse_lazy(age_gate_url)
                )

        return None

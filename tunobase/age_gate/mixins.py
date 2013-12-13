'''
Created on 23 Oct 2013

@author: michael
'''
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.conf import settings

from tunobase.age_gate import utils

class AgeGateMixin(object):
    '''
    Mixin to check if the User is old enough to view the content
    '''
    age_gate_url = getattr(settings, 'AGE_GATE_URL', 'age_gate')
    raise_exception = False  # Default whether to raise an exception to none

    def dispatch(self, request, *args, **kwargs):
        age_gate_passed = request.session.get('age_gate_passed', False)

        if not age_gate_passed:
            if self.raise_exception:  # *and* if an exception was desired
                raise PermissionDenied  # return a forbidden response.
            else:
                return utils.redirect_to_age_gate(
                    request.get_full_path(), 
                    reverse_lazy(self.age_gate_url)
                )

        return super(AgeGateMixin, self).dispatch(request, *args, **kwargs)

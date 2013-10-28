'''
Created on 23 Oct 2013

@author: michael
'''
import datetime

from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.conf import settings

from tunobase.age_gate import utils

class AgeGateMixin(object):
    '''
    Mixin to check if the User is old enough to view the content
    '''
    age_gate_url = 'age-gate'
    raise_exception = False  # Default whether to raise an exception to none

    def dispatch(self, request, *args, **kwargs):
        age_gate_passed = request.session.get('age_gate_passed', False)
        
        if not age_gate_passed:
            if self.raise_exception:  # *and* if an exception was desired
                raise PermissionDenied  # return a forbidden response.
            else:
                return utils.redirect_to_age_gate(request.get_full_path(), self.age_gate_url)

        return super(AgeGateMixin, self).dispatch(request, *args, **kwargs)
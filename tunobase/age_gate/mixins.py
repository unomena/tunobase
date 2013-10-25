'''
Created on 23 Oct 2013

@author: michael
'''
from django.core.exceptions import ImproperlyConfigured, PermissionDenied

from tunobase.age_gate import utils

class AgeGateMixin(object):
    '''
    Mixin to check if the User is old enough to view the content
    '''
    age_gate_url = 'age-gate'
    raise_exception = False  # Default whether to raise an exception to none

    def dispatch(self, request, *args, **kwargs):
        user_date_of_birth = request.session.get('user_date_of_birth')
        country_date_of_birth_required = request.session.get('country_date_of_birth_required')
        
        if user_date_of_birth is not None and country_date_of_birth_required is not None:
            if  user_date_of_birth > country_date_of_birth_required:  # If the user is a standard user,
                if self.raise_exception:  # *and* if an exception was desired
                    raise PermissionDenied  # return a forbidden response.
                else:
                    return utils.redirect_to_age_gate(request.get_full_path(), self.age_gate_url)
        else:
            if self.raise_exception:  # *and* if an exception was desired
                raise PermissionDenied  # return a forbidden response.
            else:
                return utils.redirect_to_age_gate(request.get_full_path(), self.age_gate_url)

        return super(AgeGateMixin, self).dispatch(request, *args, **kwargs)
'''
Created on 23 Oct 2013

@author: michael
'''
from django.core.exceptions import ImproperlyConfigured, PermissionDenied

from tunobase.eula import models, utils

class EULAAcceptedMixin(object):
    eula_url = None
    raise_exception = False  # Default whether to raise an exception to none

    def dispatch(self, request, *args, **kwargs):
        try:
            if request.user.eula_accepted.version != models.EULA.permitted.latest_eula().version:  # If the user is a standard user,
                if self.raise_exception:  # *and* if an exception was desired
                    raise PermissionDenied  # return a forbidden response.
                else:
                    return utils.redirect_to_eula(request.get_full_path(),
                        self.eula_url)
        except AttributeError:
            if self.raise_exception:  # *and* if an exception was desired
                raise PermissionDenied  # return a forbidden response.
            else:
                return utils.redirect_to_eula(request.get_full_path(),
                    self.eula_url)

        return super(EULAAcceptedMixin, self).dispatch(request,
            *args, **kwargs)
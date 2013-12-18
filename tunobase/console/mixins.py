"""
CONSOLE APP

This module provides extra functionality to be used with the rest of
the app.

Classes:
    ConsoleUserRequiredMixin

Functions:
    n/a

Created on 25 Oct 2013

@author: michael

"""
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.utils.decorators import method_decorator

class ConsoleUserRequiredMixin(object):
    """Mixin allows you to require a user with `is_console_user`
    set to True.

    """
    login_url = settings.LOGIN_URL  # LOGIN_URL from project settings
    raise_exception = False  # Default whether to raise an exception to none
    redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        If the user is not allowed to access the console, return
        Forbidden reponse.

        """
        # If the user is a standard user,
        if not request.user.can_access_console:
            if self.raise_exception:  # *and* if an exception was desired
                raise PermissionDenied  # return a forbidden response.
            else:
                return redirect_to_login(
                    request.get_full_path(),
                    self.login_url,
                    self.redirect_field_name
                )

        return super(ConsoleUserRequiredMixin, self)\
                .dispatch(request, *args, **kwargs)

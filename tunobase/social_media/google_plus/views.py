"""
GOOGLE PLUS APP

This module provides an interface for users to interact with
the Google Plus app.

Classes:
    PreLogin
    LoginCallback

Functions:
    n/a

Created on 29 Oct 2013

@author: michael

"""
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.http import unquote
from django.views import generic as generic_views

class PreLogin(generic_views.View):
    """Set up URLs for Google Plus login."""

    def get(self, request, *args, **kwargs):
        """Set up URLs for Google Plus login."""
        if not reverse('secure_login') in request.META['HTTP_REFERER']:
            request.session['google_plus_login_redirect_url'] = \
                    request.META['HTTP_REFERER']

        return redirect(unquote(request.GET['auth_url']))


class LoginCallback(generic_views.View):
    """Set up post URLs for after login."""

    def get(self, request, *args, **kwargs):
        """Set up post URLs for after login."""
        from tunobase.social_media.google_plus import utils
        credential = utils.FLOW.step2_exchange(request.REQUEST)
        redirect_url = request.session.get(
            'google_plus_login_redirect_url',
            settings.LOGIN_REDIRECT_URL
        )
        user = authenticate(
            credential=credential,
        )

        if user is None:
            raise ValidationError("Invalid Login")

        if not user.is_active:
            raise ValidationError("User is inactive")

        auth_login(request, user)

        return redirect(redirect_url)

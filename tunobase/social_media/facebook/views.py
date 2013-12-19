"""
FACEBOOK APP

This module provides an interface for the user to interact
with the Facebook app.

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
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.http import unquote
from django.views import generic as generic_views

import facebook

class PreLogin(generic_views.View):
    """Set up URLs to login with."""

    def get(self, request, *args, **kwargs):
        """Set up login url."""

        if not reverse('secure_login') in request.META['HTTP_REFERER']:
            request.session['facebook_login_redirect_url'] = \
                    request.META['HTTP_REFERER']

        return redirect(unquote(request.GET['auth_url']))


class LoginCallback(generic_views.View):
    """Set up URLs to return to."""

    def get(self, request, *args, **kwargs):
        """Set up success url."""

        redirect_url = settings.LOGIN_REDIRECT_URL
        if not 'error' in request.GET and \
           request.session['facebook_state'] == request.GET['state']:
            login_redirect_uri = 'http://%s%s' % (
                Site.objects.get_current().domain,
                reverse('facebook_login_callback')
            )
            access_token = facebook.get_access_token_from_code(
                request.GET['code'],
                login_redirect_uri,
                settings.FACEBOOK_APP_ID,
                settings.FACEBOOK_APP_SECRET
            )
            redirect_url = request.session.get(
                'facebook_login_redirect_url',
                settings.LOGIN_REDIRECT_URL
            )
            user = authenticate(
                access_token=access_token['access_token'],
                access_token_expiry_seconds=access_token['expires']
            )

            if user is None:
                raise ValidationError("Invalid Login")

            if not user.is_active:
                raise ValidationError("User is inactive")

            auth_login(request, user)

        return redirect(redirect_url)

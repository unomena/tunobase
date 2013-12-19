"""
TWITTER APP

This app provides an interface for users to interact with
the twitter app.

Classes:
    PreLogin
    LoginCallback
    RequestEmail

Functions:
    n/a

Created on 29 Oct 2013

@author: michael

"""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views import generic as generic_views

from twython import Twython

from tunobase.core import mixins as core_mixins

class PreLogin(generic_views.View):
    """Set up urls to login in with."""

    def get(self, request, *args, **kwargs):
        """Set up urls to login in with."""

        twitter = Twython(
            settings.TWITTER_APP_KEY,
            settings.TWITTER_APP_SECRET
        )
        login_redirect_uri = 'http://%s%s' % (
            Site.objects.get_current().domain,
            reverse('twitter_login_callback')
        )
        auth = twitter.get_authentication_tokens(
            callback_url=login_redirect_uri
        )

        request.session['twitter_oauth_token'] = auth['oauth_token']
        request.session['twitter_oauth_token_secret'] = \
                auth['oauth_token_secret']
        if not reverse('secure_login') in request.META['HTTP_REFERER']:
            request.session['twitter_login_redirect_url'] = \
                    request.META['HTTP_REFERER']

        return redirect(auth['auth_url'])


class LoginCallback(generic_views.View):
    """
    Manage users logging in and authenticating
    via Twitter.

    """

    def get(self, request, *args, **kwargs):
        """
        Manage users logging in and authenticating
        via Twitter.

        """
        oauth_verifier = request.GET['oauth_verifier']

        twitter = Twython(
            settings.TWITTER_APP_KEY,
            settings.TWITTER_APP_SECRET,
            request.session['twitter_oauth_token'],
            request.session['twitter_oauth_token_secret']
        )

        final_step = twitter.get_authorized_tokens(oauth_verifier)

        twitter_oauth_token = final_step['oauth_token']
        twitter_oauth_token_secret = final_step['oauth_token_secret']
        redirect_url = request.session.get(
            'twitter_login_redirect_url',
            settings.LOGIN_REDIRECT_URL
        )
        user = authenticate(
            twitter_oauth_token=twitter_oauth_token,
            twitter_oauth_token_secret=twitter_oauth_token_secret
        )

        if user is None:
            raise ValidationError("Invalid Login")

        if not user.is_active:
            raise ValidationError("User is inactive")

        auth_login(request, user)

        if user.email is None and settings.TWITTER_EMAIL_REQUIRED:
            return redirect('twitter_request_email')

        return redirect(redirect_url)


class RequestEmail(core_mixins.LoginRequiredMixin, generic_views.UpdateView):
    """Allow users to update their email addresses."""

    def get_object(self):
        """Return a user object."""

        return self.request.user

    def form_valid(self, form):
        """Upon validation save form."""

        self.object = form.save()

        messages.success(self.request, 'Profile details updated.')

        return redirect(settings.LOGIN_REDIRECT_URL)

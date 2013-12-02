'''
Created on 29 Oct 2013

@author: michael
'''
from django.views import generic as generic_views
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.sites.models import Site
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login as auth_login
from django.core.exceptions import ValidationError
from django.contrib import messages

from twython import Twython

from tunobase.core import mixins as core_mixins

class PreLogin(generic_views.View):
    
    def get(self, request, *args, **kwargs):
        twitter = Twython(
            settings.TWITTER_APP_KEY, 
            settings.TWITTER_APP_SECRET
        )
        login_redirect_uri = 'http://%s%s' % (
            Site.objects.get_current().domain, 
            reverse_lazy('twitter_login_callback')
        )
        auth = twitter.get_authentication_tokens(
            callback_url=login_redirect_uri
        )
        
        request.session['twitter_oauth_token'] = auth['oauth_token']
        request.session['twitter_oauth_token_secret'] = auth['oauth_token_secret']
        request.session['twitter_login_redirect_url'] = request.META['HTTP_REFERER']
        
        return redirect(auth['auth_url'])

class LoginCallback(generic_views.View):
    
    def get(self, request, *args, **kwargs):
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
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        self.object = form.save()
        
        messages.success(self.request, 'Profile details updated.')

        return redirect(settings.LOGIN_REDIRECT_URL)
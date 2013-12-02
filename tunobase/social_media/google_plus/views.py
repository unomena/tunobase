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
from django.utils.http import unquote

from apiclient.discovery import build

class PreLogin(generic_views.View):
    
    def get(self, request, *args, **kwargs):
        request.session['google_plus_login_redirect_url'] = request.META['HTTP_REFERER']
        
        return redirect(unquote(request.GET['auth_url']))

class LoginCallback(generic_views.View):
    
    def get(self, request, *args, **kwargs):
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
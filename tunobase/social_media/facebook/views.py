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

import facebook

class PreLogin(generic_views.View):
    
    def get(self, request, *args, **kwargs):
        request.session['facebook_login_redirect_url'] = request.META['HTTP_REFERER']
        
        return redirect(unquote(request.GET['auth_url']))

class LoginCallback(generic_views.View):
    
    def get(self, request, *args, **kwargs):
        redirect_url = settings.LOGIN_REDIRECT_URL
        if not 'error' in request.GET and \
           request.session['facebook_state'] == request.GET['state']:
            login_redirect_uri = 'http://%s%s' % (
                Site.objects.get_current().domain, 
                reverse_lazy('facebook_login_callback')
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
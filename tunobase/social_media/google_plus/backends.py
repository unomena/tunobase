'''
Created on 09 Nov 2013

@author: michael
'''
import httplib2
import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404
 
from flufl.password import generate
 
from tunobase.social_media.google_plus import models
 
class GooglePlusBackend(object):
    '''
    Authenticate against a Facebook access token
    '''
 
    supports_inactive_user = False
 
    def authenticate(self, credential=None):
        if not credential.invalid:
            http = httplib2.Http()
            http = credential.authorize(http)
            response_headers, response_body = http.request('https://www.googleapis.com/oauth2/v1/userinfo?alt=json')
            #print response_headers, response_body
            #response_headers = json.loads(response_headers)
            response_body = json.loads(response_body)
            
            print response_body
            
            #if not response_headers['status'] == '200':
            #    raise Exception('An error occurred with the Request to Google')
            
            try:
                google_plus_user = models.GooglePlusUser.objects.get(
                    google_user_id=response_body['id']
                )
                 
                google_plus_user.update_access_token(
                    credential.access_token,
                    credential.token_expiry,
                    credential.refresh_token,
                    credential.id_token,
                    credential.token_response
                )
                 
                user = google_plus_user.user
            except models.GooglePlusUser.DoesNotExist:
                # Create a new user.
                user = get_user_model().objects.create(
                    username=response_body['email'],
                    email=response_body['email'],
                    is_regular_user=False,
                    is_active=True,
                    first_name=response_body['given_name'],
                    last_name=response_body['family_name'],
                )
                user.set_password(generate(10))
                user.save()
                  
                google_plus_user = models.GooglePlusUser(
                    user=user,
                    google_user_id=response_body['id']
                )
                google_plus_user.update_access_token(
                    credential.access_token,
                    credential.token_expiry,
                    credential.refresh_token,
                    credential.id_token,
                    credential.token_response
                )
                 
            return user
         
        return None
 
    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
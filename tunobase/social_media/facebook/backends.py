'''
Created on 09 Nov 2013

@author: michael
'''
from django.conf import settings
from django.contrib.auth import get_user_model

from flufl.password import generate

import facebook

from tunobase.social_media.facebook import models, utils

class FacebookBackend(object):
    '''
    Authenticate against a Facebook access token
    '''

    supports_inactive_user = False

    def authenticate(self, access_token=None, access_token_expiry_seconds=None):
        token_valid, user_id = utils.validate_access_token(access_token)
        
        if token_valid:
            try:
                facebook_user = models.FacebookUser.objects.get(
                    facebook_user_id=user_id
                )
                
                facebook_user.update_access_token(
                    access_token,
                    access_token_expiry_seconds
                )
                
                user = facebook_user.user
            except models.FacebookUser.DoesNotExist:
                # Create a new user.
                api = facebook.GraphAPI(access_token)
                email = api.get_object('me')['email']
                user = get_user_model().objects.create_user(
                    email=email, 
                    password=generate(10),
                    is_regular_user=False
                )
                 
                facebook_user = models.FacebookUser(
                    user=user,
                    facebook_user_id=user_id
                )
                facebook_user.update_access_token(
                    access_token,
                    access_token_expiry_seconds
                )
                
            return user
        
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
"""
FACEBOOK APP

This module authenticates against Facebook access tokens.

Classes:
    FacebookBackend

Functions:
    n/a

Created on 09 Nov 2013

@author: michael

"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from flufl.password import generate

import facebook

from tunobase.social_media.facebook import models, utils

class FacebookBackend(ModelBackend):
    """Authenticate against a Facebook access token."""

    supports_inactive_user = False

    def authenticate(self, access_token=None,
            access_token_expiry_seconds=None):
        """
        If the users access token is valid, update their token
        in the database.

        """
        token_valid, user_id = utils.validate_access_token(access_token)

        if token_valid:
            try:
                facebook_user = models.FacebookUser.objects.get(
                    facebook_user_id=str(user_id)
                )

                facebook_user.update_access_token(
                    access_token,
                    access_token_expiry_seconds
                )

                user = facebook_user.user
            except models.FacebookUser.DoesNotExist:
                # Create a new user.
                api = facebook.GraphAPI(access_token)
                api_data = api.get_object('me')
                user, created = get_user_model().objects.get_or_create(
                    email=api_data['email'],
                    defaults={
                        'username': api_data['username'],
                        'is_regular_user': False,
                        'is_active': True,
                        'first_name': api_data['first_name'],
                        'last_name': api_data['last_name'],
                        'city': api_data['location']['name'] if 'location' \
                                in api_data else None
                    }
                )
                if created:
                    user.set_password(generate(10))
                    user.save()

                facebook_user = models.FacebookUser(
                    user=user,
                    facebook_user_id=str(user_id)
                )
                facebook_user.update_access_token(
                    access_token,
                    access_token_expiry_seconds
                )

            return user

        return None

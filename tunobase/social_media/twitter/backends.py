'''
Created on 09 Nov 2013

@author: michael
'''
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from flufl.password import generate

from twython import Twython

from tunobase.social_media.twitter import models

class TwitterBackend(ModelBackend):
    '''
    Authenticate against a Facebook access token
    '''

    supports_inactive_user = False

    def authenticate(self, twitter_oauth_token=None,
            twitter_oauth_token_secret=None):
        twitter = Twython(
            settings.TWITTER_APP_KEY,
            settings.TWITTER_APP_SECRET,
            twitter_oauth_token,
            twitter_oauth_token_secret
        )
        verification_details = twitter.verify_credentials()

        if verification_details:
            try:
                twitter_user = models.TwitterUser.objects.get(
                    screen_name=verification_details['screen_name']
                )

                twitter_user.update_oauth_token(
                    twitter_oauth_token,
                    twitter_oauth_token_secret
                )

                user = twitter_user.user
            except models.TwitterUser.DoesNotExist:
                # Create a new user.
                first_name = verification_details['name'].split(' ')[0]
                last_name = ' '.join(
                        verification_details['name'].split(' ')[1:]
                )
                user = get_user_model().objects.create(
                    username=verification_details['screen_name'],
                    is_regular_user=False,
                    is_active=True,
                    first_name=first_name,
                    last_name=last_name,
                    city=verification_details['location'] \
                            if 'location' in verification_details else None
                )
                user.set_password(generate(10))
                user.save()

                twitter_user = models.TwitterUser(
                    user=user,
                    screen_name=verification_details['screen_name']
                )
                twitter_user.update_oauth_token(
                    twitter_oauth_token,
                    twitter_oauth_token_secret
                )

            return user

        return None

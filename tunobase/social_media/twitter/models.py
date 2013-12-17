'''
Created on 08 Nov 2013

@author: michael
'''
from django.conf import settings
from django.db import models

class TwitterUser(models.Model):
    user = models.OneToOneField(
            settings.AUTH_USER_MODEL, related_name='twitter_user'
    )
    screen_name = models.CharField(max_length=255)
    oauth_token = models.CharField(max_length=255)
    oauth_token_secret = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % self.user

    def update_oauth_token(self, oauth_token, oauth_token_secret):
        '''
        Update the access token and timestamp
        '''
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.save()

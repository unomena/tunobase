"""
FACEBOOK APP

This module describes the Facebook models.

Classes:
    FacebookUser

Functions:
    n/a

Created on 08 Nov 2013

@author: michael

"""
import datetime

from django.conf import settings
from django.db import models

class FacebookUser(models.Model):
    """Returns the FacebookUser fields."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
            related_name='facebook_user')
    facebook_user_id = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    access_token_expiry_timestamp = models.DateTimeField()

    def __unicode__(self):
        """Returns user object."""

        return u'%s' % self.user

    def update_access_token(self, access_token, access_token_expiry_seconds):
        """Update the access token and timestamp."""

        self.access_token = access_token
        self.access_token_expiry_timestamp = datetime.datetime.utcnow() + \
            datetime.timedelta(seconds=int(access_token_expiry_seconds))
        self.save()

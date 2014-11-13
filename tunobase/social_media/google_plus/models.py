"""
GOOGLE PLUS APP

This module describes the GooglePlusUser model.

Classes:
    GooglePlusUser

Functions:
    n/a

Created on 08 Nov 2013

@author: michael

"""
from django.conf import settings
from django.db import models
 
class GooglePlusUser(models.Model):
    """Returns the GooglePlusUser fields."""

    user = models.OneToOneField(
            settings.AUTH_USER_MODEL, related_name='google_plus_user'
    )
    google_user_id = models.CharField(max_length=255)
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    id_token = models.TextField()
    token_response = models.TextField()
    access_token_expiry_timestamp = models.DateTimeField()

    def __unicode__(self):
        """Returns the user object."""
        return u'%s' % self.user

    def update_access_token(self, access_token, access_token_expiry_timestamp, 
                            refresh_token, id_token, token_response):
        """Update the access token and timestamp."""

        self.access_token = access_token
        self.access_token_expiry_timestamp = access_token_expiry_timestamp
        self.refresh_token = refresh_token
        self.id_token = id_token
        self.token_response = token_response
        self.save()

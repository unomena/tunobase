'''
Created on 08 Nov 2013

@author: michael
'''
from django.db import models
from django.utils import timezone
from django.conf import settings

class FacebookUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='facebook_user')
    facebook_user_id = models.PositiveIntegerField()
    access_token = models.CharField(max_length=255)
    access_token_expiry_timestamp = models.DateTimeField()
    
    def __unicode__(self):
        return u'%s' % self.user
    
    def update_access_token(self, access_token, access_token_expiry_seconds):
        '''
        Update the access token and timestamp
        '''
        self.access_token = access_token
        self.access_token_expiry_timestamp = timezone.now() + \
            timezone.timedelta(seconds=int(access_token_expiry_seconds))
        self.save()
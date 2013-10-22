'''
Created on 22 Oct 2013

@author: michael
'''
from django.db import models
from django.conf import settings

class OutboundEmail(models.Model):
    '''
    Tracks emails sent to Users by the system.
    '''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='outbound_emails', 
        blank=True, 
        null=True
    )
    subject = models.CharField(max_length=250)
    message = models.TextField()
    sent_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_timestamp']
        
    def __unicode__(self):
        return u'%s - %s' % (self.sent_timestamp, self.subject)
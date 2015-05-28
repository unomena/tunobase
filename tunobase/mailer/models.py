"""
MAILER APP

This module describes the data layout for the mailer app.

Classes:
    OutboundEmail

Functions:
    n/a

Created on 22 Oct 2013

@author: michael

"""
from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site

from redactor.fields import RedactorTextField


class OutboundEmail(models.Model):
    """Tracks emails sent to Users by the system."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='outbound_emails',
        blank=True,
        null=True
    )
    to_addresses = models.TextField()
    bcc_addresses = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=250)
    message = RedactorTextField()
    sent_timestamp = models.DateTimeField(auto_now_add=True)
    site = models.ForeignKey(Site)

    class Meta:
        """Order by sent timestamp."""

        ordering = ['-sent_timestamp']

    def __unicode__(self):
        """Return the timestamp and subject of the mailer."""

        return u'%s - %s' % (self.sent_timestamp, self.subject)

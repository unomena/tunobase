"""
CONTACT APP

This modules sets up the database structure for the contact app.

Classes:
    ContactMessage

Functions:
    n/a

Created on 23 Oct 2013

@author: michael

"""
from django.db import models
from django.contrib.sites.models import Site
from django.conf import settings

from tunobase.corporate.company_info.contact import signals

class ContactMessage(models.Model):
    """Contact message sent from the Site."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=16, blank=True, null=True)
    message = models.TextField()
    site = models.ForeignKey(Site, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        """Return a unicode object."""

        return u'%s'  % self.name

    def send(self):
        """Fire off signal to be received by handlers."""

        signals.contact_message_saved.send(
            sender=self.__class__,
            contact_message_id=self.id
        )

    def save(self, *args, **kwargs):
        """ Save contact form."""

        if self.site is None:
            self.site = Site.objects.get_current()
        super(ContactMessage, self).save(*args, **kwargs)

        self.send()

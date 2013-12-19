"""
EULA APP

This module describes the database layout for the EULA models.

Classes:
    EULA
    EULAVersion
    UserEULA

Functions:
    n/a

Created on 06 Mar 2013

@author: michael

"""
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models

from ckeditor.fields import RichTextField

from tunobase.core import models as core_models
from tunobase.eula import managers

class EULA(models.Model):
    """Provides the title and site the EULA is to be used on."""

    title = models.CharField(max_length=255, default='')
    sites = models.ManyToManyField(Site, blank=True, null=True)

    objects = managers.EULAManager()

    def latest_version(self):
        """Fetch the latest version according to publish date."""

        try:
            return self.instances.permitted().order_by('-publish_at')[0]
        except IndexError:
            return None

    def __unicode__(self):
        """Returns the EULA title."""

        return u'%s - %s' % (self.title, self.sites.all())

class EULAVersion(core_models.StateModel, core_models.AuditModel):
    """Store various EULA versions."""

    eula = models.ForeignKey(EULA, related_name='instances')
    content = RichTextField()
    version = models.CharField(max_length=255)

    objects = managers.EULAVersionManager()

    class Meta:
        """Order by published date."""

        ordering = ['-publish_at']

    def __unicode__(self):
        """Return the EULA and its version."""

        return u'%s Version %s' % (self.eula, self.version)

class UserEULA(models.Model):
    """Link the user to the EULA they accepted."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='signed_eulas')
    eula = models.ForeignKey(EULAVersion)

    ip_address = models.IPAddressField()
    signed_at = models.DateTimeField(auto_now_add=True)
    eula_content_copy = RichTextField()
    content_type = models.ForeignKey(
        ContentType,
        related_name="content_type_set_for_%(class)s",
        blank=True,
        null=True
    )
    object_pk = models.PositiveIntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey(
        ct_field="content_type", 
        fk_field="object_pk",
    )

    class Meta:
        """Link the user to the EULA they accepted."""

        unique_together = ('user', 'eula')

    def __unicode__(self):
        """Return the user and EULA they accepted."""

        return u'%s - %s' % (self.user, self.eula)

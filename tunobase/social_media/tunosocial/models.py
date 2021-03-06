"""
TUNOSOCIAL APP

This module describes how the tunosocial app is laid out.

Classes:
    BaseLikeAbstractModel

Functions:
    n/a

Created on 08 Nov 2013

@author: michael

"""
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core import urlresolvers
from django.db import models

from tunobase.social_media.tunosocial import managers

class BaseLikeAbstractModel(models.Model):
    """
    An abstract base class that any custom like models probably should
    subclass.

    """
    # Content-object field
    content_type = models.ForeignKey(
        ContentType,
        related_name="content_type_set_for_%(class)s"
    )
    object_pk = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey(
            ct_field="content_type", fk_field="object_pk"
    )

    # Metadata about the tag
    site = models.ForeignKey(Site)

    class Meta:
        abstract = True

    def get_content_object_url(self):
        """
        Get a URL suitable for redirecting to the content object.
        """
        return urlresolvers.reverse(
            "likes-url-redirect",
            args=(self.content_type_id, self.object_pk)
        )


class Like(BaseLikeAbstractModel):
    """Set up the Social like fields."""

    user = models.ForeignKey(
            settings.AUTH_USER_MODEL, related_name='tunosocial_likes',
            blank=True, null=True
    )
    ip_address = models.IPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = managers.LikeManager()

    class Meta:
        unique_together = ('user', 'content_type', 'object_pk')

    def __unicode__(self):
        """Return the user, content_type and object_pk."""

        return u'%s - %s %s' % (self.user, self.content_type, self.object_pk)

"""
TAGGING APP

This module describes the tagging app's data layer.

"""
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from django.core import urlresolvers
from django.db import models

from tunobase.core.models import SlugModel
from tunobase.tagging import managers

class BaseTagAbstractModel(models.Model):
    """
    An abstract base class that any custom tag models probably should
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
            "tags-url-redirect",
            args=(self.content_type_id, self.object_pk)
        )


class Tag(SlugModel):
    """Unique tags on the Site."""

    description = models.TextField(null=True, blank=True)
    site = models.ForeignKey(Site, blank=True, null=True)

    objects = managers.TagManager()

    class Meta:
        unique_together = [('title', 'site')]

    def __unicode__(self):
        """Return tag's title and site."""

        return u'%s - %s' %  (self.title, self.site)


class ContentObjectTag(BaseTagAbstractModel):
    "ContentObjectTag fields."""

    tag = models.ForeignKey(Tag, related_name='content_object_tags')

    objects = managers.ContentObjectTagManager()

    def __unicode__(self):
        """Return content_type, object_pk and tag's title."""

        return u'%s %s - %s' % (
                self.content_type, self.object_pk, self.tag.title
        )

    def save(self, *args, **kwargs):
        """Set the site before saving."""

        if self.site is None:
            self.site = Site.objects.get_current()
        super(ContentObjectTag, self).save(*args, **kwargs)

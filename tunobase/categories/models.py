"""
CATEGORIES APP

This module describes the categories app's data layer.

"""
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from django.core import urlresolvers
from django.db import models

class BaseCategoryAbstractModel(models.Model):
    """
    An abstract base class that any custom category models probably should
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

    # Metadata about the category
    site = models.ForeignKey(Site)

    class Meta:
        abstract = True


class Category(models.Model):
    """Unique categories on the Site."""

    title = models.CharField(max_length=32, db_index=True)
    description = models.TextField(null=True, blank=True)
    site = models.ForeignKey(Site, blank=True, null=True)

    class Meta:
        unique_together = [('title', 'site')]

    def __unicode__(self):
        """Return category's title and site."""

        return u'%s - %s' %  (self.title, self.site)


class ContentObjectCategory(BaseCategoryAbstractModel):
    "ContentObjectCategory fields."""

    category = models.ForeignKey(Category, related_name='content_object_categories')

    def __unicode__(self):
        """Return content_type, object_pk and category's title."""

        return u'%s %s - %s' % (
                self.content_type, self.object_pk, self.category.title
        )

    def save(self, *args, **kwargs):
        """Set the site before saving."""

        if self.site is None:
            self.site = Site.objects.get_current()
        super(ContentObjectCategory, self).save(*args, **kwargs)

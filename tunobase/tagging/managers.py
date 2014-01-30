"""
TAGGING APP

This module provides a series of managers to manage
the tagging app.

"""
from django.contrib.contenttypes.models import ContentType
from django.db import models

from tunobase.core import managers as core_managers

class ContentObjectTagManager(models.Manager):
    """Retrieve various information about an objects tags."""

    def get_tags_for_object(self, obj, site=None):
        """Fetch all the tags for an object."""

        return super(ContentObjectTagManager, self)\
                .get_query_set()\
                .select_related('tag')\
                .filter(
                    content_type=ContentType.objects.get_for_model(obj),
                    object_pk=obj.pk,
                    site=site
                )

    def get_unique_tags_for_object_type(self, app_label, model, site=None):
        """Fetch all unique tags for an object."""

        tags = set()
        content_object_tags = super(ContentObjectTagManager, self)\
                .get_query_set()\
                .select_related('tag')\
                .filter(
                    content_type=ContentType.objects\
                            .get_by_natural_key(app_label, model),
                    site=site
                )

        for content_object_tag in content_object_tags:
            tags.add(content_object_tag.tag.title)

        return tags

    def get_tag_counts_for_object_type(self, app_label, model, site=None):
        """Fetch the tag count."""
        tags = self.get_unique_tags_for_object_type(app_label, model, site)
        tag_counter_dict = {}

        for tag in tags:
            title = tag.title
            if title in tag_counter_dict:
                tag_counter_dict[title] += 1
            else:
                tag_counter_dict[title] = 1

        return tag_counter_dict


class TagManager(core_managers.CoreManager):
    pass

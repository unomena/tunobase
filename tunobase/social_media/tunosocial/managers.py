"""
TUNOSOCIAL APP

This module provides a series of managers for interacting with
the tunosocial app.

Classes:
    LikeManager

Functions:
    n/a

Created on 28 Oct 2013

@author: michael

"""
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models

class LikeManager(models.Manager):
    """Manage how users are able to interact with the Like mechanism."""

    def get_num_likes_for_object(self, obj, site=None):
        """Retrieve the number of likes an object has received."""

        if site is None:
            site = Site.objects.get_current()

        return self.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_pk=obj.pk,
            site=site
        ).count()

    def get_already_liked(self, user, obj, site=None):
        """
        Return a flag stating whether an object has already
        been liked.

        """
        if site is None:
            site = Site.objects.get_current()

        queryset = self.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_pk=obj.pk,
            site=site
        )

        return queryset.filter(
            user=user
        ).exists()

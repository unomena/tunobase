"""
CORE APP

This module provides an interface to the app's managers.

"""
from django.db import models
from django.utils import timezone

from polymorphic import PolymorphicManager

from tunobase.core import constants, query

# Normal managers

class CoreManager(models.Manager):
    """Return relevant objects."""

    def get_queryset(self):
        """Return objects."""

        return query.CoreQuerySet(self.model, using=self._db)

    def for_current_site(self):
        """Return objects for the current site."""

        return self.get_queryset().for_current_site()


class CoreStateManager(CoreManager):
    """Return relevant objects depending on state."""

    def get_queryset(self):
        """Return objects."""
        return query.CoreStateQuerySet(self.model, using=self._db)

    def publish_objects(self):
        """Return only published objects."""

        queryset = self.permitted().filter(
            publish_at__lte=timezone.now()
        ).exclude(state=constants.STATE_PUBLISHED)

        queryset.update(state=constants.STATE_PUBLISHED)

    def permitted(self):
        """Only return publised objects."""

        return self.get_queryset().permitted()


# Polymorphic Managers

class CorePolymorphicManager(PolymorphicManager, CoreManager):

    def get_queryset(self):
        return query.CorePolymorphicQuerySet(self.model, using=self._db)


class CorePolymorphicStateManager(CorePolymorphicManager, CoreStateManager):

    def get_queryset(self):
        return query.CorePolymorphicStateQuerySet(self.model, using=self._db)


# Other Managers

class DefaultImageManager(CoreStateManager):

    def get_queryset(self):
        return query.DefaultImageQuerySet(self.model, using=self._db)

    def get_random(self, category=None):
        return self.get_queryset().get_random(category)

"""
CORE APP

This module provides an interface to the app's managers.

"""
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

# from polymorphic import PolymorphicManager

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

    def get_list(self):
        return self.get_queryset().get_list()

    def get_console_queryset(self):
        return self.get_queryset().get_console_queryset()

    def version_list(self, object_id, state):
        series = self.get_series(object_id)
        if series is not None:
            qs = series.versions.filter(state=state)
            for model in qs:
                model.change_url = reverse('%s_%s_change' % (
                    model.content_object._meta.app_label,
                    model.content_object._meta.module_name),
                    args=(model.object_id,)
                )
            return qs
        return []

    def get_series(self, object_id):
        from tunobase.core.models import Version
        model_type = ContentType.objects.get_for_model(self.model)
        try:
            return Version.objects.get(
                content_type__pk=model_type.id,
                object_id=object_id
            ).series
        except:
            return None

    def add_series(self, slug):
        from tunobase.core.models import VersionSeries
        return VersionSeries.objects.create(
            slug=slug
        )

    def add_version(self, obj):
        from tunobase.core.models import Version
        model_type = ContentType.objects.get_for_model(self.model)
        series = self.add_series(slugify(str(obj)))
        Version.objects.create(
            content_type=model_type,
            object_id=obj.pk,
            series=series,
            number=1,
            state=obj.state
        )

    def add_to_series(self, series, obj):
        from tunobase.core.models import Version
        model_type = ContentType.objects.get_for_model(self.model)
        try:
            latest_version_number = Version.objects.filter(
                series=series
            ).order_by('-number')[0].number + 1
        except:
            latest_version_number = 1

        Version.objects.create(
            content_type=model_type,
            object_id=obj.pk,
            series=series,
            number=latest_version_number,
            state=constants.STATE_UNPUBLISHED
        )

    def stage_version(self, object_id):
        from tunobase.core.models import Version
        series = self.get_series(object_id)
        model_type = ContentType.objects.get_for_model(self.model)
        if series is not None and Version.objects.filter(
                series=series, state=constants.STATE_STAGED).exists():
            staged_version = Version.objects.get(
                series=series,
                state=constants.STATE_STAGED
            )
            staged_version.state = constants.STATE_UNPUBLISHED
            staged_version.save()
            staged_version.content_object.state = constants.STATE_UNPUBLISHED
            staged_version.content_object.save()

        version = Version.objects.get(
            content_type__pk=model_type.id,
            object_id=object_id
        )
        version.state = constants.STATE_STAGED
        version.save()
        version.content_object.state = constants.STATE_STAGED
        version.content_object.save()

    def publish_version(self, object_id):
        from tunobase.core.models import Version
        series = self.get_series(object_id)
        model_type = ContentType.objects.get_for_model(self.model)

        if series is not None and Version.objects.filter(
                series=series, state=constants.STATE_PUBLISHED).exists():
            published_version = Version.objects.get(
                series=series,
                state=constants.STATE_PUBLISHED
            )
            published_version.state = constants.STATE_UNPUBLISHED
            published_version.save()
            published_version.content_object.state = constants.STATE_UNPUBLISHED
            published_version.content_object.save()
        version = Version.objects.get(
            content_type__pk=model_type.id,
            object_id=object_id
        )
        version.state = constants.STATE_PUBLISHED
        version.save()
        version.content_object.state = constants.STATE_PUBLISHED
        version.content_object.save()

    def unpublish_version(self, object_id):
        from tunobase.core.models import Version
        model_type = ContentType.objects.get_for_model(self.model)

        version = Version.objects.get(
            content_type__pk=model_type.id,
            object_id=object_id
        )
        version.state = constants.STATE_UNPUBLISHED
        version.save()
        version.content_object.state = constants.STATE_UNPUBLISHED
        version.content_object.publish_date_time = timezone.now()
        version.content_object.save()

    def delete_version(self, object_id):
        from tunobase.core.models import Version
        model_type = ContentType.objects.get_for_model(self.model)

        version = Version.objects.get(
            content_type__pk=model_type.id,
            object_id=object_id
        )
        version.state = constants.STATE_DELETED
        version.save()
        version.content_object.state = constants.STATE_DELETED
        version.content_object.save()


# # Polymorphic Managers
# 
# class CorePolymorphicManager(PolymorphicManager, CoreManager):
# 
#     def get_queryset(self):
#         return query.CorePolymorphicQuerySet(self.model, using=self._db)
# 
# 
# class CorePolymorphicStateManager(CorePolymorphicManager, CoreStateManager):
# 
#     def get_queryset(self):
#         return query.CorePolymorphicStateQuerySet(self.model, using=self._db)


# Other Managers

class DefaultImageManager(CoreStateManager):

    def get_queryset(self):
        return query.DefaultImageQuerySet(self.model, using=self._db)

    def get_random(self, category=None):
        return self.get_queryset().get_random(category)

'''
CORE APP

Defines custom queryset objects

'''
import random

from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType

# from polymorphic import PolymorphicQuerySet

from tunobase.core import constants


class CoreQuerySet(QuerySet):

    def for_current_site(self):
        key = '%s__id__exact' % 'sites' if hasattr(self.model, 'sites') \
                else 'site_id'
        params = {
            key: Site.objects.get_current().id
        }
        return self.filter(**params)


class CoreStateQuerySet(CoreQuerySet):
    STATE = constants.STATE_PUBLISHED
    NEXT_STATE = constants.STATE_STAGED
    BOTTOM_STATE = constants.STATE_UNPUBLISHED
    SITE_STATE = constants.STATE_STAGED if settings.STAGING else \
        constants.STATE_PUBLISHED

    def get_list(self):
        from tunobase.core.models import Version
        model_type = ContentType.objects.get_for_model(self.model)
        model_qs = Version.objects.filter(
            content_type__pk=model_type.id,
            state=self.STATE
        )
        model_pks = model_qs.values_list('object_id', flat=True)
        model_series = model_qs.values_list('series_id', flat=True)
        next_model_qs = Version.objects.filter(
            content_type__pk=model_type.id,
            state=self.NEXT_STATE
        ).exclude(series_id__in=model_series)
        next_model_pks = next_model_qs.values_list('object_id', flat=True)
        next_model_series = next_model_qs.values_list('series_id', flat=True)
        bottom_model_qs = Version.objects.filter(
            content_type__pk=model_type.id,
            state=self.BOTTOM_STATE
        ).exclude(series_id__in=list(model_series) + list(next_model_series))
        series_ids = {}
        bottom_model_pks = []
        for bottom_model in bottom_model_qs:
            if bottom_model.series_id not in series_ids:
                series_ids[bottom_model.series_id] = None
                bottom_model_pks.append(bottom_model.object_id)
        return self.filter(
            pk__in=list(model_pks) + list(next_model_pks) + list(bottom_model_pks)
        ).exclude(state=constants.STATE_DELETED)

    def get_console_queryset(self):
        from tunobase.core.models import Version
        model_type = ContentType.objects.get_for_model(self.model)
        model_pks = Version.objects.filter(
            content_type__pk=model_type.id,
        ).values_list('object_id', flat=True)
        return self.filter(pk__in=model_pks).exclude(
            state=constants.STATE_DELETED
        )

    def permitted(self):
        from tunobase.core.models import Version
        model_type = ContentType.objects.get_for_model(self.model)
        states = [self.SITE_STATE]
        if self.SITE_STATE == 2:
            states = constants.PERMITTED_STATE
        model_pks = Version.objects.filter(
            content_type__pk=model_type.id,
            state__in=states
        ).values_list('object_id', flat=True)
        return self.filter(pk__in=model_pks).exclude(
            state=constants.STATE_DELETED
        )


# class CorePolymorphicQuerySet(PolymorphicQuerySet, CoreQuerySet):
#     pass
# 
# 
# class CorePolymorphicStateQuerySet(PolymorphicQuerySet, CoreStateQuerySet):
#     pass


class DefaultImageQuerySet(CoreStateQuerySet):

    def get_random(self, category=None):
        pre_def_images = self.filter(category=category)
        if pre_def_images:
            return random.choice(pre_def_images).image
        else:
            return None

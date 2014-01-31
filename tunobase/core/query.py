'''
CORE APP

Defines custom queryset objects

'''
import random

from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models.query import QuerySet

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

    def permitted(self):
        queryset = self.filter(
            state__in=constants.PERMITTED_STATE
        )
 
        # exclude objects in staging state if not in staging mode 
        # (settings.STAGING = False)
        if not getattr(settings, 'STAGING', False):
            queryset = queryset.exclude(state=constants.STATE_STAGED)
 
        return queryset


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

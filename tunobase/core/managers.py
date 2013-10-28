'''
Created on 25 Oct 2013

@author: michael
'''
import random

from django.db import models, IntegrityError
from django.contrib.sites.models import Site
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.db.models import signals
from django.conf import settings

from polymorphic import PolymorphicManager

from tunobase.core import constants

class SiteObjectsManagerMixin(models.Manager):
    
    def for_current_site(self):
        key = '%s__id__exact' % 'sites' if hasattr(self, 'sites') else 'site'
        params = {
            key: Site.objects.get_current().id
        }
        return super(SiteObjectsManagerMixin, self).get_query_set().filter(**params)

class SiteObjectsManager(PolymorphicManager, SiteObjectsManagerMixin):
    pass

class StateManagerMixin(models.Manager):
    
    def publish_objects(self):
        queryset = super(StateManagerMixin, self).get_query_set().filter(
            publish_at__lte=timezone.now()
        ).exclude(state=constants.STATE_PUBLISHED)
        
        queryset.update(state=constants.STATE_PUBLISHED)

    def get_query_set(self):
        queryset = super(StateManagerMixin, self).get_query_set().filter(
            state__in=[constants.STATE_PUBLISHED, constants.STATE_STAGED]
        )
            
        # exclude objects in staging state if not in staging mode (settings.STAGING = False)
        if not getattr(settings, 'STAGING', False):
            queryset = queryset.exclude(state=constants.STATE_STAGED)
        return queryset
    
class StateManager(StateManagerMixin, SiteObjectsManager):
    pass

class DefaultImageManager(StateManagerMixin):

    def get_random(self, category=None):
        pre_def_images = self.filter(category=category)
        if pre_def_images:
            return random.choice(pre_def_images).image
        else:
            return None
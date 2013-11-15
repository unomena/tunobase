'''
Created on 25 Oct 2013

@author: michael
'''
import random

from django.db import models
from django.contrib.sites.models import Site
from django.utils import timezone
from django.conf import settings

from polymorphic import PolymorphicManager

from tunobase.core import constants, query

# Normal managers
    
class CoreManager(models.Manager):
    
    def get_queryset(self):
        return query.CoreQuerySet(self.model, using=self._db)
    
class CoreStateManager(CoreManager):
    
    def get_queryset(self):
        return query.CoreStateQuerySet(self.model, using=self._db)
    
    def publish_objects(self):
        queryset = self.filter(
            publish_at__lte=timezone.now()
        ).exclude(state=constants.STATE_PUBLISHED)
        
        queryset.update(state=constants.STATE_PUBLISHED)

    def permitted(self):
        return self.get_queryset().permitted()

# Polymorphic Managers
    
class CorePolymorphicManager(PolymorphicManager):
    
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
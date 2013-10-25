'''
Created on 25 Oct 2013

@author: michael
'''
from django.db import models
from django.utils import timezone

from tunobase.core import managers as core_managers

class EventManagerMixin(models.Manager):
    
    def current_events(self):
        return super(EventManagerMixin, self).get_query_set().filter(
            end__gte=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        )
        
    def past_events(self):
        return super(EventManagerMixin, self).get_query_set().filter(
            end__lt=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        )

class PermittedEventManager(core_managers.StateManager, EventManagerMixin):
    pass

class EventManager(core_managers.SiteObjectsManager, EventManagerMixin):
    pass
'''
Created on 25 Oct 2013

@author: michael
'''
from tunobase.core import managers as core_managers
from tunobase.corporate.media import query

class EventManager(core_managers.CorePolymorphicStateManager):

    def get_queryset(self):
        return query.EventQuerySet(self.model, using=self._db)

    def current_and_future_events(self):
        return self.get_queryset().current_and_future_events()

    def past_events(self):
        return self.get_queryset().past_events()

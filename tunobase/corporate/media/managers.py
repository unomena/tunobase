"""
MEDIA APP

This module provides an interface for the media app to
be able to access events posted at certain stages.
Eg current and future events and past events.

Classes:
    EventManager

Functions:
    n/a

Created on 25 Oct 2013

@author: michael

"""
from tunobase.core import managers as core_managers
from tunobase.corporate.media import query

class EventManager(core_managers.CorePolymorphicStateManager):
    """
    Provide methods to be able to access events posted at
    certain times easier.

    """

    def get_queryset(self):
        """Return event object."""

        return query.EventQuerySet(self.model, using=self._db)

    def current_and_future_events(self):
        """Return all current and future events."""

        return self.get_queryset().current_and_future_events()

    def past_events(self):
        """Return all past events."""

        return self.get_queryset().past_events()

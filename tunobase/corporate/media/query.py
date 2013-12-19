"""
MEDIA APP

This module provides an interface into querying for
events that occur in the past or are current or are to
occur in the future.

Classes:
    EventQuerySet

Functions:
    n/a

Created on 25 Oct 2013

@author: michael

"""
from django.utils import timezone

from tunobase.core import query as core_query

class EventQuerySet(core_query.CorePolymorphicStateQuerySet):
    """Provide a set of queries relating to events."""

    def current_and_future_events(self):
        """
        Query the db for events occuring currently or in the
        future.

        """
        return self.filter(
            end__gte=timezone.now()\
                    .replace(hour=0, minute=0, second=0, microsecond=0)
        )

    def past_events(self):
        """Query the db for events occuring in the past."""

        return self.filter(
            end__lt=timezone.now()\
                    .replace(hour=0, minute=0, second=0, microsecond=0)
        )

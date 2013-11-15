'''
Created on 25 Oct 2013

@author: michael
'''
from tunobase.core import query as core_query
    
class EventQuerySet(core_query.CorePolymorphicStateQuerySet):
    
    def current_and_future_events(self):
        return self.filter(
            end__gte=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        )
        
    def past_events(self):
        return self.filter(
            end__lt=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        )
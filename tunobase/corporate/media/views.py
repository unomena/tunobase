'''
Created on 23 Oct 2013

@author: michael
'''
from django.views import generic as generic_views

from tunobase.corporate.media import models

class Articles(generic_views.ListView):
    
    def get_queryset(self):
        return models.Article.permitted.for_current_site()
    
class PressReleases(generic_views.ListView):
    
    def get_queryset(self):
        return models.PressRelease.permitted.for_current_site()
    
class MediaCoverage(generic_views.ListView):
    
    def get_queryset(self):
        return models.MediaCoverage.permitted.for_current_site()
    
class Events(generic_views.ListView):
    
    def get_context_data(self, **kwargs):
        context = super(Events, self).get_context_data(**kwargs)
        
        context.update({
            'current_and_future_events': models.Event.permitted.current_and_future_events(),
            'past_events': models.Event.permitted.past_events(),
            'object_list': models.Event.permitted.for_current_site()
        })
        
        return context
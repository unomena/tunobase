'''
Created on 26 Mar 2013

@author: michael
'''
from django.db import models
from django.contrib.sites.models import Site

from tunobase.core import models as core_models, managers as core_managers

class PollQuestion(core_models.StateModel):
    question = models.CharField(max_length=1024)
    multiple_choice = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, db_index=True)
    sites = models.ManyToManyField(Site, blank=True, null=True)
    
    permitted = core_managers.SiteObjectsStateManagerMixin()
    
    class Meta:
        ordering = ['order']
    
    def __unicode__(self):
        return u'%s' % self.question
    
class PollAnswer(models.Model):
    poll = models.ForeignKey(PollQuestion, related_name='answers')
    answer = models.CharField(max_length=1024)
    vote_count = models.PositiveIntegerField(default=0)
    
    def __unicode__(self):
        return u'%s' % self.answer
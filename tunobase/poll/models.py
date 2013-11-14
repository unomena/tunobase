'''
Created on 26 Mar 2013

@author: michael
'''
from django.db import models
from django.contrib.sites.models import Site

from tunobase.core import models as core_models, managers as core_managers, \
    constants as core_constants

class PollQuestion(core_models.StateModel):
    question = models.CharField(max_length=1024)
    multiple_choice = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, db_index=True)
    sites = models.ManyToManyField(Site, blank=True, null=True)
    
    objects = models.Manager()
    permitted = core_managers.SiteObjectsStateManagerMixin()
    
    class Meta:
        ordering = ['order', '-publish_at']
    
    def __unicode__(self):
        return u'%s - %s' % (self.question, self.sites.all())
    
    @property
    def permitted_answers(self):
        return self.answers.filter(state__in=core_constants.PERMITTED_STATE)
    
class PollAnswer(core_models.StateModel):
    poll = models.ForeignKey(PollQuestion, related_name='answers')
    answer = models.CharField(max_length=1024)
    vote_count = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0, db_index=True)
    sites = models.ManyToManyField(Site, blank=True, null=True)
    
    objects = models.Manager()
    permitted = core_managers.SiteObjectsStateManagerMixin()
    
    class Meta:
        ordering = ['order', 'answer']
    
    def __unicode__(self):
        return u'%s' % self.answer
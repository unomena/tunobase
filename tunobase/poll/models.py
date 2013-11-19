'''
Created on 26 Mar 2013

@author: michael
'''
from django.db import models
from django.contrib.sites.models import Site
from django.conf import settings

from tunobase.core import models as core_models
from tunobase.poll import managers

class PollQuestion(core_models.ImageModel, core_models.StateModel):
    question = models.CharField(max_length=1024)
    multiple_choice = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, db_index=True)
    sites = models.ManyToManyField(Site, blank=True, null=True)
    
    class Meta:
        ordering = ['order', '-publish_at']
    
    def __unicode__(self):
        return u'%s - %s' % (self.question, self.sites.all())
    
class PollAnswer(core_models.StateModel):
    poll = models.ForeignKey(PollQuestion, related_name='answers')
    answer = models.CharField(max_length=1024)
    vote_count = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0, db_index=True)
    sites = models.ManyToManyField(Site, blank=True, null=True)
    users_answered = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='polls_answered',
        blank=True, 
        null=True
    )
    
    objects = managers.PollAnswerManager()
    
    class Meta:
        ordering = ['order', 'answer']
    
    def __unicode__(self):
        return u'%s' % self.answer
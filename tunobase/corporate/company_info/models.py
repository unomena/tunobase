'''
Created on 23 Oct 2013

@author: michael
'''
from django.db import models
from django.contrib.sites.models import Site
from django.conf import settings

from tunobase.core import models as core_models

class ContactMessage(models.Model):
    '''
    Contact message sent from the Site
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=16, blank=True, null=True)
    message = models.TextField()
    site = models.ForeignKey(Site, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return u'%s'  % self.name

class Vacancy(core_models.ContentModel):
    '''
    Job vacancies within the company
    '''
    external_link = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Vacancies'
    
class CompanyMemberPosition(core_models.StateModel, core_models.SlugModel):
    '''
    Member positions within the Company
    '''
    sites = models.ManyToManyField(Site, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    
    def __unicode__(self):
        return u'%s' % self.title
    
    class Meta:
        ordering = ['order']

class CompanyMember(core_models.ContentModel):
    '''
    Members of the company
    '''
    default_image_category = 'company_member'
    
    positions = models.ManyToManyField(CompanyMemberPosition, related_name='company_members')
    job_title = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    
    class Meta:
        ordering = ['order']
'''
Created on 06 Mar 2013

@author: michael
'''
from django.db import models
from django.contrib.sites.models import Site

from ckeditor.fields import RichTextField

from tunobase.core import models as core_models
from tunobase.eula import managers

class EULA(models.Model):
    title = models.CharField(max_length=255, default='')
    sites = models.ManyToManyField(Site, blank=True, null=True)
    
    objects = managers.EULAManager()
    
    def latest_version(self):
        try:
            return self.instances.permitted().order_by('-publish_at')[0]
        except IndexError:
            return None
    
    def __unicode__(self):
        return u'%s' % self.title
    
class EULAVersion(core_models.StateModel, core_models.AuditModel):
    eula = models.ForeignKey(EULA, related_name='instances')
    content = RichTextField()
    version = models.CharField(max_length=255)
    
    permitted = managers.EULAVersionManager()
    
    class Meta:
        ordering = ['-publish_at']
    
    def __unicode__(self):
        return u'%s Version %s' % (self.eula, self.version)
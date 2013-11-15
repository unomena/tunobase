'''
Created on 06 Mar 2013

@author: michael
'''
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings

from ckeditor.fields import RichTextField

from tunobase.core import models as core_models, constants as core_constants
from tunobase.eula import managers

class EULA(models.Model):
    title = models.CharField(max_length=255, default='')
    sites = models.ManyToManyField(Site, blank=True, null=True)
    
    objects = managers.EULAManager()
    
    def latest_version(self):
        try:
            return self.instances.filter(state__in=core_constants.PERMITTED_STATE)\
                .order_by('-publish_at')[0]
        except IndexError:
            return None
    
    def __unicode__(self):
        return u'%s - %s' % (self.title, self.sites.all())
    
class EULAVersion(core_models.StateModel, core_models.AuditModel):
    eula = models.ForeignKey(EULA, related_name='instances')
    content = RichTextField()
    version = models.CharField(max_length=255)
    
    objects = managers.EULAVersionManager()
    
    class Meta:
        ordering = ['-publish_at']
    
    def __unicode__(self):
        return u'%s Version %s' % (self.eula, self.version)
    
class UserEULA(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='signed_eulas')
    eula = models.ForeignKey(EULAVersion)
    
    ip_address = models.IPAddressField()
    signed_at = models.DateTimeField(auto_now_add=True)
    eula_content_copy = RichTextField()
    content_type = models.ForeignKey(
        ContentType,
        related_name="content_type_set_for_%(class)s",
        blank=True,
        null=True
    )
    object_pk = models.PositiveIntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey(
        ct_field="content_type", 
        fk_field="object_pk",
    )
    
    class Meta:
        unique_together = ('user', 'eula')
    
    def __unicode__(self):
        return u'%s - %s' % (self.user, self.eula)
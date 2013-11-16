'''
Created on 28 Oct 2013

@author: michael
'''
import json

from django.db import models

from tunobase.core import models as core_models
from tunobase.bulk_loading import managers

class BulkUploadHash(models.Model):
    '''
    Records hashes of bulk uploaded CSV files allowing us to track
    duplicate imports and warn users accordingly.
    '''
    md5 = models.CharField(max_length=32)
    
    def __unicode__(self):
        return u'%s' % self.md5
    
class BulkUploadData(models.Model):
    data = models.TextField()
    
    objects = managers.BulkUploadDataManager()
    
    def __unicode__(self):
        return u'%s' % self.data
    
    def save(self, *args, **kwargs):
        if not self.id and self.data:
            self.data = json.dumps(self.data)
        super(BulkUploadData, self).save(*args, **kwargs)
    
class BulkUploadImage(core_models.AuditModel):
    image = models.ImageField(upload_to='bulk_upload_images')
    has_been_attached = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'%s' % self.image
'''
Created on 25 Oct 2013

@author: michael
'''
import json

from django.db import models
    
class BulkUploadDataManager(models.Manager):
    
    def get_decoded_data(self, pk):
        try:
            obj = self.get_queryset().get(pk=pk)
            return json.loads(obj.data), obj
        except self.model.DoesNotExist:
            return None, None
'''
Created on 28 Oct 2013

@author: michael
'''
from django.db import transaction
from django.core.exceptions import ImproperlyConfigured

class BulkUpdater(object):
    data_key = None
    model = None
    
    def __init__(self, data_to_upload):
        self.data_to_upload = data_to_upload
    
    def get_object(self, data):
        if self.data_key is None:
            raise ImproperlyConfigured(
                "Attribute 'data_key' is not set"
            )
            
        if self.model is None:
            raise ImproperlyConfigured(
                "Attribute 'model' is not set"
            )
        
        try:
            kwargs = {
                self.data_key: data[self.data_key]
            }
            return self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            return None
    
    def bulk_create_objects(self, object_list):
        return NotImplemented
    
    def create_object(self, data):
        return NotImplemented
    
    def update_object(self, obj, data, created):
        return NotImplemented
    
    @transaction.atomic
    def save(self, create, update):
        '''
        Save uploaded objects
        '''
        # If we're only creating objects, then bulk
        # insert them to optimize performance
        if create and not update:
            objs = []
            for data in self.data_to_upload:
                obj = self.create_object(data)
                objs.append(obj)
                
            try:
                self.bulk_create_objects(objs)
            except ValueError:
                # Object was inherited model and we can't use bulk create
                for obj in objs:
                    obj.save()
        else:
            for data in self.data_to_upload:
                created = False
                
                obj = self.get_object(data)
    
                if obj is None and create:
                    obj = self.create_object(data)
                    created = True
    
                if created or update:
                    # Set simple fields.
                    self.update_object(obj, data, created)
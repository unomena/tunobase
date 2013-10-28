'''
Created on 28 Oct 2013

@author: michael
'''
from django.db import models

class BulkUploadHash(models.Model):
    '''
    Records hashes of bulk uploaded CSV files allowing us to track
    duplicate imports and warn users accordingly.
    '''
    md5 = models.CharField(max_length=32)
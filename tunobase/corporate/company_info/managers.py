'''
Created on 03 Nov 2013

@author: michael
'''
from django.db import models

class NewsletterRecipientManager(models.Manager):
    
    def get_query_set(self):
        return super(NewsletterRecipientManager, self).get_query_set()\
            .filter(is_active=True)
        
        
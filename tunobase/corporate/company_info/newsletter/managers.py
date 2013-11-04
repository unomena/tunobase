'''
Created on 03 Nov 2013

@author: michael
'''
from django.db import models
from django.utils import timezone
from django.conf import settings

class NewsletterManager(models.Manager):
    
    def send_due(self):
        due_newsletters = super(NewsletterManager, self).get_query_set()\
            .select_related(
                'rich_header', 'rich_footer', 'plain_header', 'plain_footer'
            ).filter(
                send_at__lte=timezone.now()
            ).exclude(sent=True)
        
        for newsletter in due_newsletters:
            newsletter.send()

class NewsletterRecipientManager(models.Manager):
    
    def get_query_set(self):
        return super(NewsletterRecipientManager, self).get_query_set()\
            .filter(is_active=True)
        
        
'''
Created on 23 Oct 2013

@author: michael
'''
from django.dispatch import Signal
from django.dispatch import receiver

from tunobase.corporate.company_info.newsletter import tasks

# A newsletter has been saved
newsletter_saved = Signal(providing_args=["sender", "newsletter"])

@receiver(newsletter_saved)
def send_newsletter(sender, **kwargs):
    newsletter = kwargs.pop('newsletter', None)
    
    if newsletter is not None:
        tasks.email_active_newsletter_recipients(
            newsletter.subject, 
            newsletter.rich_content, 
            newsletter.plain_content,
            newsletter.id
        )
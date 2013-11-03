'''
Created on 23 Oct 2013

@author: michael
'''
from django.dispatch import Signal
from django.dispatch import receiver

from tunobase.corporate.company_info import tasks

# A newsletter has been saved
newsletter_saved = Signal(providing_args=["sender", "newsletter"])
# A contact message has been saved
contact_message_saved = Signal(providing_args=["sender", "contact_message_id"])

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

@receiver(contact_message_saved)
def send_contact_message(sender, **kwargs):
    contact_message_id = kwargs.pop('contact_message_id', None)
    
    if contact_message_id is not None:
        tasks.email_contact_message(contact_message_id)
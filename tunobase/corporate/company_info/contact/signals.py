'''
Created on 23 Oct 2013

@author: michael
'''
from django.dispatch import Signal, receiver

from tunobase.corporate.company_info.contact import tasks

# A contact message has been saved
contact_message_saved = Signal(providing_args=["sender", "contact_message_id"])

@receiver(contact_message_saved)
def send_contact_message(sender, **kwargs):
    contact_message_id = kwargs.pop('contact_message_id', None)
    
    if contact_message_id is not None:
        tasks.email_contact_message(contact_message_id)
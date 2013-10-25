'''
Created on 23 Oct 2013

@author: michael
'''
from django.dispatch import Signal
from django.dispatch import receiver

from tunobase.corporate.company_info import tasks

# A contact message has been sent
contact_message_saved = Signal(providing_args=["sender", "user_id", "contact_message_id"])

@receiver(contact_message_saved)
def send_contact_message(sender, **kwargs):
    user_id = kwargs.pop('user_id', None)
    contact_message_id = kwargs.pop('contact_message_id', None)
    
    if contact_message_id is not None:
        tasks.email_contact_message(user_id, contact_message_id)
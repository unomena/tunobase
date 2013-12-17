'''
Created on 21 Oct 2013

@author: michael
'''
from celery.decorators import task

from django.conf import settings

from tunobase.mailer import utils as mailer_utils

@task(default_retry_delay=10 * 60)
def email_contact_message(contact_message_id):
    '''
    Sends a Contact Message email to the Site's owners/support team
    '''
    try:
        from tunobase.corporate.company_info.contact import models

        contact_message = models.ContactMessage.objects.get(
            pk=contact_message_id
        )
        user = contact_message.user

        ctx_dict = {
            'contact_message' : contact_message,
        }

        mailer_utils.send_mail(
            subject='email/subjects/contact_message_subject.txt',
            html_content='email/html/contact_message.html',
            text_content='email/txt/contact_message.txt',
            context=ctx_dict,
            to_addresses=[settings.CONTACT_MESSAGE_TO_EMAIL,],
            user=user
        )
    except Exception, exc:
        raise email_contact_message.retry(exc=exc)

'''
Created on 21 Oct 2013

@author: michael
'''
from celery.decorators import task

from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.conf import settings

from tunobase.mailer import utils as mailer_utils

@task(ignore_result=True)
def email_active_newsletter_recipients(subject, html_content, text_content, 
                                       newsletter_id=None):
    '''
    Sends active newsletter recipients the Newsletter content
    '''
    from tunobase.corporate.company_info import models
        
    active_newsletter_recipients = models.NewsletterRecipient.active_recipients.all()
    bcc_addresses = ['dev@unomena.com']
    messages = []
    contexts = []
    
    # Create messages for each newsletter recipient
    for newsletter_recipient in active_newsletter_recipients:
        message, context = mailer_utils.create_message(
            subject=subject, 
            html_content=html_content, 
            text_content=text_content,
            to_addresses=[newsletter_recipient.get_email()],
            bcc_addresses=bcc_addresses,
            user=newsletter_recipient.user
        )
        messages.append(message)
        contexts.append(context)
    
    # Bulk send the messages
    mailer_utils.send_messages(messages)
    
    # Bulk track the messages
    outbound_emails = []
    for message, context in zip(messages, contexts):
        outbound_email = mailer_utils.create_outbound_email(
            message.subject, 
            message.to,
            html_content,
            bcc_addresses,
            context['site'],
            context['user']
        )
        outbound_emails.append(outbound_email)
        
    mailer_utils.save_outbound_emails(outbound_emails)
    
    # If a Newsletter id was supplied we will save the
    # sent emails to the recipients
    if newsletter_id is not None:
        newsletter = models.Newsletter.objects.get(id=newsletter_id)
        newsletter.recipients.add(*list(active_newsletter_recipients))

@task(default_retry_delay=10 * 60)
def email_contact_message(contact_message_id):
    '''
    Sends a Contact Message email to the Site's owners/support team
    '''
    try:
        from tunobase.corporate.company_info import models
        
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
            bcc_addresses=['dev@unomena.com'],
            user=user
        )
    except Exception, exc:
        raise email_contact_message.retry(exc=exc)
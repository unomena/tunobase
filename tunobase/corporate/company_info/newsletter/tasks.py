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
    from tunobase.corporate.company_info.newsletter import models, utils
        
    active_newsletter_recipients = models.NewsletterRecipient.active_recipients.all()
    bcc_addresses = ['dev@unomena.com']
    messages = []
    contexts = []
    
    # Create messages for each newsletter recipient
    for newsletter_recipient in active_newsletter_recipients:
        uid, token = utils.get_uid_and_token(newsletter_recipient)
        ctx_dict = {
            'uid': uid,
            'token': token
        }
        message, context = mailer_utils.create_message(
            subject=subject, 
            context=ctx_dict,
            html_content=html_content, 
            text_content=text_content,
            to_addresses=[newsletter_recipient.get_email()],
            bcc_addresses=bcc_addresses,
            user=newsletter_recipient.user,
            apply_context_to_string=True
        )
        
        messages.append(message)
        contexts.append(context)
    
    # Bulk send the messages
    mailer_utils.send_messages(messages)
    
    # Bulk track the messages
    outbound_emails = []
    for message, context in zip(messages, contexts):
        # Check if the content is actual content or a location to a file
        # containing the content and render the content from that file
        # if it is
        subject, text_content, html_content = mailer_utils.render_content(
            subject,
            text_content,
            html_content,
            context,
            apply_context_to_string=True
        )
        
        # Create the Outbound Email tracker object
        outbound_email = mailer_utils.create_outbound_email(
            subject, 
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
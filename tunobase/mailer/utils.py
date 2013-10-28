'''
Created on 22 Oct 2013

@author: michael
'''
import os

from django.conf import settings
from django.core.mail import get_connection, EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from tunobase.core import utils as core_utils
from tunobase.mailer import models

def send_mail(subject, text_content, to_addresses, 
              from_address=settings.DEFAULT_FROM_EMAIL, bcc_addresses=None, 
              html_content=None, context={}, attachments=None, user=None):
    '''
    Sends an email containing both text(provided) and html(produced from
    povided template name and context) content as well as provided
    attachments to provided to_addresses from provided from_address.
    '''
    # Donot send any emails if they are disabled in the settings
    if settings.EMAIL_ENABLED:
        # Update context with site and STATIC_URL
        if not 'site' in context:
            context['site'] = Site.objects.get_current()
            
        if not 'user' in context:
            context['user'] = user
        
        context.update({
            'STATIC_URL': settings.STATIC_URL,
            'app_name': settings.APP_NAME
        })
        
        # Check if the content is actual content or a location to a file
        # containing the content and render the content from that file
        # if it is
        if core_utils.is_path(subject):
            subject = render_to_string(subject, context)
            
        if core_utils.is_path(text_content):
            text_content = render_to_string(text_content, context)
        
        if html_content is not None and core_utils.is_path(html_content):
            html_content = render_to_string(html_content, context)
        
        # Build message with text_message as default content
        msg = EmailMultiAlternatives(
            subject,
            text_content,
            from_address,
            to_addresses,
            bcc_addresses
        )
    
        if html_content is not None:
            msg.attach_alternative(html_content, "text/html")
    
        # Add attachments.
        if attachments is not None:
            for attachment in attachments:
                if attachment:
                    msg.attach(attachment.name, attachment.read())
    
        # Send message.
        connection = get_connection()
        connection.send_messages([msg, ])
        
        # Create an entry in the email tracker to track sent emails by the system
        models.OutboundEmail.objects.create(
            user=user, 
            to_addresses='\n'.join(to_addresses),
            bcc_addresses='\n'.join(bcc_addresses),
            subject=subject, 
            message=html_content,
            site=context['site']
        )
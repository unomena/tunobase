"""
MAILER APP

This module provides utility functions for use with the
mailer app.

Classes:
    n/a

Functions:
    send_messages
    render_content
    create_message
    save_outbound_emails
    create_outbound_email
    send_mail
    track_mail

Created on 22 Oct 2013

@author: michael

"""
import logging

from django.conf import settings
from django.core.mail import get_connection, EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.template.base import TemplateDoesNotExist
from django.template.loader import render_to_string

from tunobase.core import utils as core_utils
from tunobase.mailer import models

logger = logging.getLogger('console')

def send_messages(messages):
    """Bulk send the message(s)."""

    # Donot send any emails if they are disabled in the settings
    if settings.EMAIL_ENABLED:
        connection = get_connection()
        connection.send_messages(messages)
    else:
        logger.debug(
                "Not sending mail because setting 'EMAIL_ENABLED' is False"
        )

def render_content(subject, text_content, html_content=None,
                   context=None, apply_context_to_string=False):
    """Render the content in the email."""

    if context is None:
        context = {}
    try:
        subject = render_to_string(subject, context)
    except TemplateDoesNotExist:
        if apply_context_to_string:
            subject = core_utils.render_string_to_string(subject, context)

    try:
        text_content = render_to_string(text_content, context)
    except TemplateDoesNotExist:
        if apply_context_to_string:
            text_content = core_utils\
                    .render_string_to_string(text_content, context)

    if html_content is not None:
        try:
            html_content = render_to_string(html_content, context)
        except TemplateDoesNotExist:
            if apply_context_to_string:
                html_content = core_utils\
                        .render_string_to_string(html_content, context)

    return subject, text_content, html_content

def create_message(subject, text_content, to_addresses,
                   from_address=settings.DEFAULT_FROM_EMAIL,
                   bcc_addresses=None, html_content=None, context=None,
                   attachments=None, user=None, apply_context_to_string=False
    ):
    """Create and return the Email message to be sent."""

    # Update context with site and STATIC_URL
    if context is None:
        context = {}
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
    subject, text_content, html_content = render_content(
        subject,
        text_content,
        html_content,
        context,
        apply_context_to_string
    )

    # Update BCC list with extras from settings, if any
    extra_bccers = getattr(settings, 'EMAIL_EXTRA_BCC_LIST', [])
    if bcc_addresses:
        bcc_addresses = bcc_addresses + extra_bccers
    else:
        bcc_addresses = extra_bccers

    # Build message with text_message as default content
    msg = EmailMultiAlternatives(
        subject,
        text_content,
        from_address,
        to_addresses,
        bcc_addresses
    )

    # Attach HTML content
    if html_content is not None:
        msg.attach_alternative(html_content, "text/html")

    # Add attachments.
    if attachments is not None:
        for attachment in attachments:
            if attachment:
                msg.attach(attachment.name, attachment.read())

    return msg, context

def save_outbound_emails(outbound_emails):
    """Bulk create Outbound Email tracking objects."""

    if settings.EMAIL_ENABLED:
        models.OutboundEmail.objects.bulk_create(outbound_emails)

def create_outbound_email(subject, to_addresses, html_content,
                          bcc_addresses=None, site=None, user=None):
    """Create Outbound Email tracking object."""

    return models.OutboundEmail(
        user=user,
        to_addresses='\n'.join(to_addresses),
        bcc_addresses='\n'.join(bcc_addresses) \
            if bcc_addresses is not None else '',
        subject=subject,
        message=html_content,
        site=site
    )

def track_mail(subject, to_addresses, html_content,
               bcc_addresses=None, site=None, user=None):
    """Track mails sent to the User by the Site."""

    if settings.EMAIL_ENABLED:
        outbound_email = create_outbound_email(
            subject,
            to_addresses,
            html_content,
            bcc_addresses,
            site,
            user
        )
        outbound_email.save()

def send_mail(subject, text_content, to_addresses,
              from_address=settings.DEFAULT_FROM_EMAIL, bcc_addresses=None,
              html_content=None, context=None, attachments=None, user=None,
              apply_context_to_string=False):
    """
    Sends an email containing both text(provided) and html(produced from
    povided template name and context) content as well as provided
    attachments to provided to_addresses from provided from_address

    """
    # Create the message
    message, context = create_message(
        subject,
        text_content,
        to_addresses,
        from_address,
        bcc_addresses,
        html_content,
        context,
        attachments,
        user,
        apply_context_to_string
    )

    # Send the message
    send_messages([message])

    # Check if the content is actual content or a location to a file
    # containing the content and render the content from that file
    # if it is
    subject, text_content, html_content = render_content(
        subject,
        text_content,
        html_content,
        context,
        apply_context_to_string
    )

    # Create an entry in the email tracker to
    # track sent emails by the system
    track_mail(
        subject,
        to_addresses,
        html_content,
        bcc_addresses,
        context['site'],
        user
    )

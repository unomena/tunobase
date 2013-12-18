"""
NEWSLETTER APP

This module provides a task for sending off newsletters.

Classes:
    n/a

Functions:
    send_newsletter

Created on 23 Oct 2013

@author: michael

"""
from django.dispatch import Signal
from django.dispatch import receiver

from tunobase.core import utils as core_utils
from tunobase.corporate.company_info.newsletter import tasks

# A newsletter has been saved
newsletter_saved = Signal(providing_args=["sender", "newsletter"])

@receiver(newsletter_saved)
def send_newsletter(sender, **kwargs):
    """Creation of the newsletter content for sending."""

    newsletter = kwargs.pop('newsletter', None)

    if newsletter is not None:
        rich_content = \
            core_utils.not_null_str(newsletter.rich_header) + \
            core_utils.not_null_str(newsletter.rich_content) + \
            core_utils.not_null_str(newsletter.rich_footer)

        plain_content = \
            core_utils.not_null_str(newsletter.plain_header) + \
            core_utils.not_null_str(newsletter.plain_content) + \
            core_utils.not_null_str(newsletter.plain_footer)

        tasks.email_active_newsletter_recipients(
            newsletter.subject,
            rich_content,
            plain_content,
            newsletter.id
        )

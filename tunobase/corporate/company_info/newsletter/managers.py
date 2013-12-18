"""
NEWSLETTER APP

This module provides an interface for sending newsletters.

Classes:
    NewsletterManager
    NewsletterRecipientManager

Functions:
    n/a

Created on 03 Nov 2013

@author: michael

"""
from django.db import models
from django.utils import timezone

class NewsletterManager(models.Manager):
    """Retrieve newsletters that need to be send."""

    def send_due(self):
        """Retrieve newsletters that need to be send."""

        due_newsletters = super(NewsletterManager, self).get_query_set()\
            .select_related(
                'rich_header', 'rich_footer', 'plain_header', 'plain_footer'
            ).filter(
                send_at__lte=timezone.now()
            ).exclude(sent=True)

        for newsletter in due_newsletters:
            newsletter.send()


class NewsletterRecipientManager(models.Manager):
    """Retrieve newsletter recipients."""

    def get_query_set(self):
        """Retrieve newsletter recipients."""

        return super(NewsletterRecipientManager, self).get_query_set()\
            .filter(is_active=True)



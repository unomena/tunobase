"""
NEWSLETTER APP

This module describes how the newsletter models are stored.

Classes:
    RichNewsletterPart
    PlainNewsletterPart
    Newsletter
    NewsletterRecipient

Functions:
    n/a

Created on 23 Oct 2013

@author: michael

"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from redactor.fields import RedactorTextField

from tunobase.corporate.company_info.newsletter import managers, signals


class RichNewsletterPart(models.Model):
    """Rich content field for newsletter."""

    content = RedactorTextField()

    def __unicode__(self):
        """Returns a unicode object."""

        return u'%s' % self.content


class PlainNewsletterPart(models.Model):
    """Plain content field for newsletter."""

    content = models.TextField()

    def __unicode__(self):
        """Returns a unicode object."""

        return u'%s' % self.content


class Newsletter(models.Model):
    """Newsletter to send to active recipients."""

    subject = models.CharField(max_length=255)

    plain_header = models.ForeignKey(
        PlainNewsletterPart,
        related_name='newsletter_headers',
        blank=True,
        null=True
    )
    plain_content = models.TextField(blank=True, null=True)
    plain_footer = models.ForeignKey(
        PlainNewsletterPart,
        related_name='newsletter_footers',
        blank=True,
        null=True
    )
    rich_header = models.ForeignKey(
        RichNewsletterPart,
        related_name='newsletter_headers',
        blank=True,
        null=True
    )
    rich_content = RedactorTextField(blank=True, null=True)
    rich_footer = models.ForeignKey(
        RichNewsletterPart,
        related_name='newsletter_footers',
        blank=True,
        null=True
    )

    site = models.ForeignKey(Site, blank=True, null=True)
    send_at = models.DateTimeField(blank=True, null=True)
    sent = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = managers.NewsletterManager()

    def __unicode__(self):
        """Returns a unicode object."""

        return u'%s' % self.subject

    def send(self):
        """Fire off signal to be received by handlers."""

        signals.newsletter_saved.send(
            sender=self.__class__,
            newsletter=self
        )
        self.sent = True
        self.save()

    def save(self, *args, **kwargs):
        """Save newsletter in the database."""

        if self.site is None:
            self.site = Site.objects.get_current()
        super(Newsletter, self).save(*args, **kwargs)

        if not self.sent:
            if self.send_at is None or self.send_at <= timezone.now():
                self.send()


class NewsletterRecipient(models.Model):
    """
    Newsletter recipients that have subscribed
    from the Site

    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='newsletter_recipient',
        blank=True,
        null=True
    )
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=True)
    newsletters_received = models.ManyToManyField(
        Newsletter,
        related_name='recipients',
        blank=True,
        null=True
    )

    objects = models.Manager()
    active_recipients = managers.NewsletterRecipientManager()

    def __unicode__(self):
        """Returns a unicode object."""

        return u'%s' % self.get_email()

    def get_greeting_name(self):
        """Return user's name."""

        if self.user is not None:
            return self.user.first_name

        if self.first_name is not None:
            return self.first_name

        return self.email

    def get_email(self):
        """Return user's email."""

        if self.user is not None:
            return self.user.email

        return self.email

    def unsubscribe(self):
        """Mark as unsubscribed."""

        self.is_active = False
        self.save()

    def save(self, *args, **kwargs):
        """Save in database."""

        if not self.id and self.email:
            User = get_user_model()
            try:
                user = User.objects.get(email__iexact=self.email)
                if user.is_active:
                    raise ValidationError(
                        'Email address %s already exists as a \
                                User on the system' % self.email
                    )
            except User.DoesNotExist:
                pass

        super(NewsletterRecipient, self).save(*args, **kwargs)

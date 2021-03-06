"""
API App

This module provides api functionality.

"""
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone

from tunobase.api import constants
from tunobase.core import fields as core_fields


class Destination(models.Model):
    """The location to send API calls to."""

    title = models.CharField(max_length=32)
    url = models.URLField()
    username = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.title


class Service(models.Model):
    """
    Where to send API calls of a certain type and how many times
    to retry.

    """
    type = models.CharField(
        max_length=200,
        unique=True,
        choices=settings.API_REQUEST_TYPE_CHOICES
    )
    destination = models.ForeignKey(Destination, related_name='services')
    max_retries = models.PositiveSmallIntegerField(default=3)
    success_string = models.CharField(max_length=200)
    error_string = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.get_type_display()


class Request(models.Model):
    """The API request data being sent."""

    uuid = core_fields.UUIDField(editable=False)
    service = models.ForeignKey(Service)
    request_data = models.TextField()
    response_data = models.TextField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(
        choices=constants.REQUEST_STATUS_CHOICES,
        default=constants.REQUEST_STATUS_CREATED
    )
    created_timestamp = models.DateTimeField(auto_now_add=True)
    completed_timestamp = models.DateTimeField(blank=True, null=True)
    retry_count = models.PositiveSmallIntegerField(default=0)
    site = models.ForeignKey(Site, blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s' % (self.uuid, self.service)

    @property
    def send_count(self):
        """Increments the retry count by 1."""

        return self.retry_count + 1

    def complete_request(self, action):
        """
        Record the status and, if successful, the completed timestamp
        in the database.

        """
        if self.service.success_string in self.response_data:
            self.status = constants.REQUEST_STATUS_SUCCESS
            self.completed_timestamp = timezone.now()
        else:
            if self.service.error_string and \
               self.service.error_string in self.response_data:
                self.status = constants.REQUEST_STATUS_ERROR
            else:
                if self.send_count > self.service.max_retries:
                    self.status = constants.REQUEST_STATUS_ABORT
                else:
                    self.status = constants.REQUEST_STATUS_RETRY

        self.save()

    def save(self, *args, **kwargs):
        """
        Set self.site to be the current site should self.site be None.

        """
        if self.site is None:
            self.site = Site.objects.get_current()
        super(Request, self).save(*args, **kwargs)

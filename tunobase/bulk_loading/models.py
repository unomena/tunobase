"""
Bulk Loading App

This module stores bulk upload data.

"""
import json

from django.db import models

from tunobase.bulk_loading import managers
from tunobase.core import models as core_models, fields as core_fields


class BulkUploadHash(models.Model):
    """
    Records hashes of bulk uploaded CSV files allowing us to track
    duplicate imports and warn users accordingly.

    """
    md5 = models.CharField(max_length=32)

    def __unicode__(self):
        """Return unicode object."""

        return u'%s' % self.md5


class BulkUploadData(models.Model):
    """Creates a text field in the database."""

    data = models.TextField()

    objects = managers.BulkUploadDataManager()

    def __unicode__(self):
        """Return unicode object."""

        return u'%s' % self.data

    def save(self, *args, **kwargs):
        """Save uploaded data."""

        if not self.id and self.data:
            self.data = json.dumps(self.data)
        super(BulkUploadData, self).save(*args, **kwargs)


class BulkUploadImage(core_models.AuditModel):
    """Creates database entry to save uploaded image details."""

    image = models.ImageField(upload_to='bulk_upload_images')
    has_been_attached = models.BooleanField(default=False)
    uuid = core_fields.UUIDField()

    def __unicode__(self):
        """Return unicode object."""
        return u'%s' % self.image

"""
Bulk Loading App

This module fetches uploaded data and decodes it to json.

Classes:
    BulkUploadDataManager

Functions:
    n/a

Created on 25 Oct 2013

@author: michael

"""
import json

from django.db import models


class BulkUploadDataManager(models.Manager):
    """Fetches uploaded data and decodes to json."""

    def get_decoded_data(self, pk):
        """Fetch uploaded data and decode to json."""

        try:
            obj = self.get_queryset().get(pk=pk)
            return json.loads(obj.data), obj
        except self.model.DoesNotExist:
            return None, None

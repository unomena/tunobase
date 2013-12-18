"""
CORE APP

This module provides a UUID field.

Classes:
    UUIDField

Functions:
    n/a

Created on 23 Oct 2013

@author: michael

"""
import uuid

from django.db import models

class UUIDField(models.CharField):
    """Provide a UUID field."""

    def __init__(self, *args, **kwargs):
        """Initialise variables."""

        kwargs['max_length'] = kwargs.get('max_length', 64 )
        kwargs['blank'] = True
        models.CharField.__init__(self, *args, **kwargs)

    def pre_save(self, model_instance, add):
        """Object manipulation before saving."""

        if add :
            value = str(uuid.uuid1())
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(models.CharField, self).pre_save(model_instance, add)

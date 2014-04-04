"""
CORE APP

This module provides a UUID field.

"""
import uuid

from django.db import models

class UUIDField(models.CharField):
    """Provide a UUID field."""

    def __init__(self, *args, **kwargs):
        """Initialise variables."""

        kwargs['max_length'] = kwargs.get('max_length', 64 )
        kwargs['blank'] = True
		self.hex = kwargs.pop('hex', False)
        models.CharField.__init__(self, *args, **kwargs)

    def pre_save(self, model_instance, add):
        """Object manipulation before saving."""

        if add :
            value = self.hex and str(uuid.uuid1().hex) or str(uuid.uuid1())
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(models.CharField, self).pre_save(model_instance, add)

"""
Bulk Loading App

This module provides the form interface for allowing users to upload
various files.

"""
from io import BytesIO
import sys

from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import FILE_INPUT_CONTRADICTION
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from tunobase.bulk_loading import widgets, models


class AjaxBulkFileField(forms.FileField):
    """Upload numerous files."""

    widget = widgets.AjaxBulkFileMultiInput

    def to_python(self, data):
        """Perform various validation steps on the uploaded file.

        First check that a file was actually uploaded then check that
        it does not exceed the maximum file size. Check that a filename
        exists and finally that if a file was required, that a
        file exists.

        """

        for datum in data:
            if datum in self.empty_values:
                return None

            # UploadedFile objects should have name and size attributes.
            try:
                file_name = datum.name
                file_size = datum.size
            except AttributeError:
                raise ValidationError(
                    self.error_messages['invalid'],
                    code='invalid'
                )

            if self.max_length is not None \
               and len(file_name) > self.max_length:
                params = {
                    'max': self.max_length,
                    'length': len(file_name)
                }
                raise ValidationError(
                        self.error_messages['max_length'],
                        code='max_length',
                        params=params
                )
            if not file_name:
                raise ValidationError(
                        self.error_messages['invalid'], code='invalid'
                )
            if not self.allow_empty_file and not file_size:
                raise ValidationError(
                        self.error_messages['empty'], code='empty'
                )

        return data

    def clean(self, data, initial=None):
        """Neaten up the data received from the file upload form.

        Raise a validation error if contradictory inputs were received.
        Return cleaned_data afterwards.

        """
        if data is None:
            return False

        cleaned_data = []
        for datum in data:
            # If the widget got contradictory inputs,
            # we raise a validation error
            if datum is FILE_INPUT_CONTRADICTION:
                raise ValidationError(
                    self.error_messages['contradiction'],
                    code='contradiction'
                )
            # False means the field value should be cleared;
            # further validation is not needed.
            if datum is False:
                if not self.required:
                    return False
                # If the field is required, clearing is not possible
                # (the widget shouldn't return False data in that case
                # anyway). False is not in self.empty_value; if a False
                # value makes it this far it should be validated from here on
                # out as None (so it will be caught by the required check).
                datum = None
            if not datum and initial:
                return initial

            cleaned_data.append(datum)

        return super(forms.FileField, self).clean(cleaned_data)

    def bound_data(self, data, initial):
        """
        There is a problem with the uploaded file,
        return the original file.

        """
        if data in (None, FILE_INPUT_CONTRADICTION):
            return initial
        return data

    def _has_changed(self, initial, data):
        """Flag to confirm if data has changed."""

        if data is None:
            return False
        return True


class AjaxBulkImageField(AjaxBulkFileField):
    """Ensure only valid image formats are uploaded."""

    default_error_messages = {
        'invalid_image': _("Upload a valid image. The file you uploaded was\
                either not an image or a corrupted image."),
    }

    def to_python(self, data):
        """
        Checks that the file-upload field data contains a valid image
        (GIF, JPG, PNG, possibly others -- whatever the Python Imaging
        Library supports).
        """
        f = super(AjaxBulkImageField, self).to_python(data)
        if f is None:
            return None

        from django.utils.image import Image

        for datum in data:
            # We need to get a file object for Pillow. We might have a path
            # or we might have to read the data into memory.
            if hasattr(datum, 'temporary_file_path'):
                file = datum.temporary_file_path()
            else:
                if hasattr(datum, 'read'):
                    file = BytesIO(datum.read())
                else:
                    file = BytesIO(datum['content'])

            try:
                # load() could spot a truncated JPEG, but it loads the entire
                # image in memory, which is a DoS vector. See #3848 and
                # #18520. verify() must be called immediately after
                # the constructor.
                Image.open(file).verify()
            except Exception:
                # Pillow (or PIL) doesn't recognize it as an image.
                six.reraise(ValidationError, ValidationError(
                    self.error_messages['invalid_image'],
                    code='invalid_image',
                ), sys.exc_info()[2])
        for datum in f:
            if hasattr(datum, 'seek') and callable(datum.seek):
                datum.seek(0)
        return f


class MultiImageIDField(forms.Field):
    """Accept uploaded images."""

    widget = forms.HiddenInput

    def widget_attrs(self, widget):
        """Set up image_ids for styling of widget."""

        attrs = super(MultiImageIDField, self).widget_attrs(widget)
        attrs.update({'class': 'image_ids'})
        return attrs

    def to_python(self, value):
        """Returns a Unicode object."""

        if value in self.empty_values:
            return None
        return models.BulkUploadImage.objects\
                .filter(uuid__in=value.split(','))

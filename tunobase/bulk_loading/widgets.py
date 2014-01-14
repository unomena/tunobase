"""
Bulk Loading App

This module provides a widget interface to allow users to upload
files.

Classes:
    AjaxBulkFileInput
    AjaxBulkFileMultiInput

Functions:
    n/a

Created on 28 Oct 2013

@author: michael

"""
from django import forms
from django.utils.datastructures import MultiValueDict, MergeDict


class AjaxBulkFileInput(forms.ClearableFileInput):
    """
    Sets up upload widget with 'bulk_image' class
    name and returns file name to be displayed.

    """
    def render(self, name, value, attrs=None):
        """Add 'bulk_image' class to widget."""

        if attrs is None:
            attrs = {}
        attrs['class'] = 'bulk_image'
        return super(AjaxBulkFileInput, self).render(name, value, attrs)

    def value_from_datadict(self, data, files, name):
        """Return uploaded file name."""

        return files.get(name, None)


class AjaxBulkFileMultiInput(AjaxBulkFileInput):
    """Handle multiple uploaded files."""

    def render(self, name, value, attrs=None):
        """Add 'multiple' class to widget."""

        if attrs is None:
            attrs = {}
        attrs['multiple'] = 'multiple'
        return super(AjaxBulkFileMultiInput, self).render(name, value, attrs)

    def value_from_datadict(self, data, files, name):
        """Return list of files uploaded."""

        if isinstance(files, (MultiValueDict, MergeDict)):
            return files.getlist(name)
        return files.get(name, None)

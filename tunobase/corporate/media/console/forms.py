"""
MEDIA CONSOLE APP

This module describes how to display the media coverage form
in the console.

Classes:
    MediaCoverageForm

Functions:
    n/a

Created on 10 Jan 2013

@author: euan

"""
from django import forms

from tunobase.corporate.media import models as media_models

class MediaCoverageForm(forms.ModelForm):
    """How to display media coverage form in the console."""

    class Meta:
        """Display the media coverage model."""

        model = media_models.MediaCoverage
        fields = ['image', 'title']

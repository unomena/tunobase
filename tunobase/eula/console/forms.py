"""
EULA CONSOLE APP

This module provides authorised console users with an
interface to update EULAs.

Classes:
    EULAForm
    EULAVersionForm

Functions:
    n/a

Created on 10 Jan 2013

@author: euan

"""
from django import forms
from django.forms.models import inlineformset_factory

from tunobase.eula import models as eula_models

class EULAForm(forms.ModelForm):
    """Display the EULA model as the EULA form."""

    class Meta:
        """Display title and sites in form."""

        model = eula_models.EULA
        fields = ['title', 'sites']

class EULAVersionForm(forms.ModelForm):
    """Display a readonly version of a particular EULA."""

    class Meta:
        """Fetch readonly version of EULA from EULAVersion model."""

        model = eula_models.EULAVersion

    def __init__(self, *args, **kwargs):
        """Set up the form with readonly html attributes."""

        super(EULAVersionForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['version'].widget.attrs\
                    .update({'readonly': 'readonly'})
            self.fields['content'].widget.attrs\
                    .update({'readonly': 'readonly'})


EULAVersionFormSet = inlineformset_factory(
    eula_models.EULA,
    eula_models.EULAVersion,
    form=EULAVersionForm,
    extra=1
)

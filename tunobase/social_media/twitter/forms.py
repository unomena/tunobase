"""
TWITTER APP

This module provides a form to check that the user's email
address doesn't already exist.

Classes:
    RequestEmailForm

Functions:
    n/a

Created on 12 Nov 2013

@author: michael

"""
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

class RequestEmailForm(forms.ModelForm):
    """Retrieve user model as form."""

    class Meta:
        model = get_user_model()
        fields = ['email']

    def clean_email(self):
        """Ensure email address doesn't already exist."""

        if get_user_model().objects.filter(
           email__iexact=self.cleaned_data['email']).exists():
            raise forms.ValidationError(
                    _('This email address already exists')
            )

        return self.cleaned_data['email']

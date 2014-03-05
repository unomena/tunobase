"""
Contact App

This module sets up the forms needed to capture company info.

Classes:
    ContactMessageForm

Functions:
    n/a

Created on 23 Oct 2013

@author: michael

"""
from django import forms

from tunobase.corporate.company_info.contact import models


class ContactMessageForm(forms.ModelForm):
    """Display contact us form."""

    class Meta:
        model = models.ContactMessage
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        """Initialise variables."""
        self.user = kwargs.pop('user', None)
        super(ContactMessageForm, self).__init__(*args, **kwargs)

        if self.user is not None:
            if self.user.first_name and self.user.last_name:
                self.fields['name'].initial = '%s %s' % \
                    (self.user.first_name, self.user.last_name)

            if self.user.mobile_number:
                self.fields['mobile_number'].initial = self.user.mobile_number

            self.fields['email'].initial = self.user.email

        self.fields['name'].widget.attrs.update({'class': 'required'})
        self.fields['email'].widget.attrs.update({'class': 'required email'})
        self.fields['message'].widget.attrs.update({'class': 'required'})

    def save(self, commit=True):
        obj = super(ContactMessageForm, self).save(commit=False)
        obj.user = self.user

        if commit:
            obj.save()

        return obj

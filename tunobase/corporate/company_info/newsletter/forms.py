"""
NEWSLETTER APP

This module handles subscription functionality.

Classes:
    NewsletterSubscribeForm

Functions:
    n/a

Created on 05 Nov 2013

@author: michael

"""
from django import forms

from tunobase.corporate.company_info.newsletter import models

class NewsletterSubscribeForm(forms.ModelForm):
    """Creation of newsletter subscription form."""

    class Meta:
        """Which fields we want to display."""

        model = models.NewsletterRecipient
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        """Initialise variables."""
        
        super(NewsletterSubscribeForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email Address',
            'class': 'required email'
        })

    def save(self, request, commit=True):
        """Save newsletter form upon successfull validation."""
        obj = super(NewsletterSubscribeForm, self).save(commit=False)

        if request.user.is_authenticated():
            obj.user = request.user
            obj.save(commit)

        return obj

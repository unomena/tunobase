'''
Created on 05 Nov 2013

@author: michael
'''
from django import forms

from tunobase.corporate.company_info.newsletter import models

class NewsletterSubscribeForm(forms.ModelForm):

    class Meta:
        model = models.NewsletterRecipient
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(NewsletterSubscribeForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email Address',
            'class': 'required email'
        })

    def save(self, request, commit=True):
        obj = super(NewsletterSubscribeForm, self).save(commit=False)

        if request.user.is_authenticated():
            obj.user = request.user
            obj.save(commit)

        return obj

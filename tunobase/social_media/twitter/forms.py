'''
Created on 12 Nov 2013

@author: michael
'''
from django import forms
from django.contrib.auth import get_user_model

class RequestEmailForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email']
    
    def clean_email(self):
        if get_user_model().objects.filter(
           email__iexact=self.cleaned_data['email']).exists():
            raise forms.ValidationError('This email address already exists')
        
        return self.cleaned_data['email']
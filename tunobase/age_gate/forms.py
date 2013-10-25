'''
Created on 27 Mar 2013

@author: michael
'''
import datetime

from django import forms
from django.conf import settings

from tunobase.core import widgets as core_widgets

class AgeGateForm(forms.Form):
    location = forms.ChoiceField(choices=settings.AGE_GATE_LOCATION_CHOICES, required=False)
    date_of_birth = forms.DateField(
        widget=core_widgets.DateSelectorWidget(
            min_num_years_back=settings.AGE_GATE_MIN_NUM_YEARS_BACK,
            max_num_years_back=settings.AGE_GATE_MAX_NUM_YEARS_BACK,
            reverse_years=True
        )
    )
    terms_accept = forms.BooleanField(required=False)
    next = forms.CharField(widget=forms.HiddenInput)
        
    
    def clean_terms_accept(self):
        if not self.cleaned_data['terms_accept']:
            raise forms.ValidationError('You must accept the terms to continue')
        
        return self.cleaned_data['terms_accept']
    
    def save(self, request):
        request.session['user_date_of_birth'] = datetime.datetime(
            int(self.cleaned_data['birth_year']), 
            int(self.cleaned_data['birth_month']), 
            int(self.cleaned_data['birth_day'])
        )
        
        age = settings.AGE_GATE_COUNTRY_LEGAL_AGES[self.cleaned_data['location']]
        request.session['country_date_of_birth_required'] = \
            datetime.datetime.now() - datetime.timedelta(days=age*365)
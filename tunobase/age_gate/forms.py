"""
AGE GATE APP

This module provides a form to determine that the user meets the
required age gate.

Classes:
    AgeGateForm

Functions:
    n/a

Created on 27 Mar 2013

@author: michael

"""
import datetime

from django import forms
from django.conf import settings

from tunobase.core import widgets as core_widgets

class AgeGateForm(forms.Form):
    """
    Form for submitting the User's Age and
    determining whether they pass the Age Gate

    """
    location = forms.ChoiceField(
            choices=settings.AGE_GATE_LOCATION_CHOICES,
            required=False
    )
    date_of_birth = forms.DateField(
        widget=core_widgets.DateSelectorWidget(
            min_num_years_back=settings.AGE_GATE_MIN_NUM_YEARS_BACK,
            max_num_years_back=settings.AGE_GATE_MAX_NUM_YEARS_BACK,
            reverse_years=True
        )
    )
    terms_accept = forms.BooleanField(required=False)
    next = forms.CharField(widget=forms.HiddenInput, required=False)


    def clean_terms_accept(self):
        """Ensure that T & C 's have been selected before continuing."""

        if not self.cleaned_data['terms_accept']:
            raise forms.ValidationError(
                'You must accept the terms to continue'
            )

        return self.cleaned_data['terms_accept']

    def save(self, request):
        """
        Check if the User's Age passes the legal requirements
        for their country and let them continue if it does

        """
        age = settings\
                .AGE_GATE_COUNTRY_LEGAL_AGES[self.cleaned_data['location']]
        country_date_of_birth_required = \
            datetime.date.today() - datetime.timedelta(days=age*365)

        request.session['age_gate_passed'] = \
            self.cleaned_data['date_of_birth'] <=\
            country_date_of_birth_required

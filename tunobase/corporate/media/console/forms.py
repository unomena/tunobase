'''
Created on 10 Jan 2013

@author: euan
'''
from django import forms

from tunobase.corporate.media import models as media_models

class MediaCoverageForm(forms.ModelForm):

    class Meta:
        model = media_models.MediaCoverage
        fields = ['image', 'title']

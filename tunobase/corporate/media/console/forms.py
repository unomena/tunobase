'''
Created on 10 Jan 2013

@author: euan
'''
from django import forms
from django.forms.models import inlineformset_factory

from tunobase.bulk_loading import fields as bulk_loading_fields, widgets as bulk_loading_widgets
from tunobase.corporate.media import models as media_models
        
class MediaCoverageForm(forms.ModelForm):
    image = bulk_loading_fields.AjaxBulkImageField(widget=bulk_loading_widgets.AjaxBulkFileInput, required=False)
    image_ids = bulk_loading_fields.MultiImageIDField(required=False)
    
    class Meta:
        model = media_models.MediaCoverage
        fields = ['title']
        
    def save(self, commit=True):
        obj = super(MediaCoverageForm, self).save(commit=False)
        if self.cleaned_data['image_ids'] is not None:
            obj.image = self.cleaned_data['image_ids'][0].image
        
        obj.save()
        self.cleaned_data['image_ids'].delete()
          
        return obj

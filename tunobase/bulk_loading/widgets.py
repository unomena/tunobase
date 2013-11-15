'''
Created on 28 Oct 2013

@author: michael
'''
from django import forms
from django.utils.datastructures import MultiValueDict, MergeDict

class AjaxBulkFileInput(forms.ClearableFileInput):
    
    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['multiple'] = 'multiple'
        return super(AjaxBulkFileInput, self).render(name, value, attrs)
    
    def value_from_datadict(self, data, files, name):
        if isinstance(files, (MultiValueDict, MergeDict)):
            return files.getlist(name)
        return files.get(name, None)
        
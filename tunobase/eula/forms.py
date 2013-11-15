'''
Created on 23 Oct 2013

@author: michael
'''
from django import forms
from django.contrib.contenttypes.models import ContentType

from tunobase.core import utils as core_utils
from tunobase.eula import models

class SignEULAForm(forms.Form):
    accept = forms.BooleanField()
    next = forms.CharField(widget=forms.HiddenInput, required=False)
        
    def __init__(self, *args, **kwargs):
        self.eula = kwargs.pop('eula', None)
        self.content_type_id = kwargs.pop('content_type_id', None)
        self.object_pk = kwargs.pop('object_pk', None)
        super(SignEULAForm, self).__init__(*args, **kwargs)
    
        self.fields['accept'].widget.attrs.update({'class': 'required'})
        
    def save(self, request):
        if self.content_type_id is not None and self.object_pk is not None:
            extra_kwargs = {
                'content_type': ContentType.objects.get_for_id(self.content_type_id),
                'object_pk': self.object_pk
            }
        else:
            extra_kwargs = {}
        
        obj = models.UserEULA.objects.create(
             user=request.user, 
             eula=self.eula, 
             eula_content_copy=self.eula.content,
             ip_address=core_utils.get_client_ip(request),
             **extra_kwargs
        )
        
        return obj
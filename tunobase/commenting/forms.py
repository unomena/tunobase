'''
Created on 29 Oct 2013

@author: michael
'''
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from tunobase.commenting import models

class CommentForm(forms.Form):
    user_id = forms.IntegerField(required=False)
    user_name = forms.CharField(max_length=100, required=False)
    comment_content_type_id = forms.IntegerField()
    comment_object_pk = forms.CharField()
    comment_box = forms.CharField(max_length=512)
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CommentForm, self).__init__(*args, **kwargs)
    
    def save(self):
        if self.user is not None:
            user_id = self.user.id
        else:
            user_id = None
        
        comment = models.CommentModel.objects.create(
            user_id=user_id,
            site=Site.objects.get_current(),
            content_type_id=self.cleaned_data['comment_content_type_id'],
            object_pk=self.cleaned_data['comment_object_pk'],
            comment=self.cleaned_data['comment_box']
        )
        
        return comment
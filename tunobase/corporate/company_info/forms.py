'''
Created on 23 Oct 2013

@author: michael
'''
from django import forms

from tunobase.corporate.company_info import models, signals

class ContactMessageForm(forms.ModelForm):
    
    class Meta:
        model = models.ContactMessage
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ContactMessageForm, self).__init__(*args, **kwargs)
        
        if self.user is not None:
            if self.user.first_name and self.user.last_name:
                self.fields['name'].initial = '%s %s' % (self.user.first_name, self.user.last_name)
                
            if self.user.mobile_number:
                self.fields['mobile_number'].initial = self.user.mobile_number
                
            self.fields['email'].initial = self.user.email
        
        self.fields['name'].widget.attrs.update({'class':'required'})
        self.fields['email'].widget.attrs.update({'class':'required email'})
        self.fields['message'].widget.attrs.update({'class':'required'})
        
    def save(self, *args, **kwargs):
        obj = super(ContactMessageForm, self).save(*args, **kwargs)
        
        if self.user is not None:
            user_id = self.user.id
        else:
            user_id = None
        
        # Fire off signal to be received by handlers
        signals.contact_message_saved.send(
            sender=self.__class__,
            user_id=user_id,
            contact_message_id=obj.id
        )
        
        return obj
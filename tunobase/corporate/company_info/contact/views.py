'''
Created on 23 Oct 2013

@author: michael
'''
from django.views import generic as generic_views
from django.core.urlresolvers import reverse

class Contact(generic_views.CreateView):
    
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(Contact, self).get_form_kwargs(*args, **kwargs)
        
        if self.request.user.is_authenticated():
            kwargs.update({'user': self.request.user})
            
        return kwargs
    
    def get_success_url(self):
        return reverse('company_info_contact_thanks')
'''
Created on 05 Mar 2013

@author: michael
'''
import datetime

from django.views import generic as generic_views
from django.http import HttpResponseRedirect
from django.conf import settings

class AgeGate(generic_views.FormView):
    
    def get_initial(self):
        return {'next': self.request.GET.get('next')}
    
    def form_valid(self, form):
        self.request.session['user_date_of_birth'] = datetime.datetime(
           int(form.cleaned_data['birth_year']), 
           int(form.cleaned_data['birth_month']), 
           int(form.cleaned_data['birth_day'])
        )
        
        age = settings.AGE_GATE_COUNTRY_LEGAL_AGES[form.cleaned_data['location']]
        
        self.request.session['country_date_of_birth_required'] = datetime.datetime.now() - datetime.timedelta(days=age*365)
        
        return HttpResponseRedirect(self.request.POST.get('next') or '/')
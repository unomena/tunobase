'''
Created on 05 Mar 2013

@author: michael
'''
from django.views import generic as generic_views
from django.http import HttpResponseRedirect

class AgeGate(generic_views.FormView):
    '''
    View the User gets sent to when an Age Gate
    is encountered
    '''

    def get_initial(self):
        return {'next': self.request.GET.get('next')}

    def get_success_url(self):
        return self.request.POST.get('next') or '/'

    def form_valid(self, form):
        form.save(self.request)

        return HttpResponseRedirect(self.get_success_url())

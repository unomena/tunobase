"""
This module deals with age gate functionality. Direct the user to the
age gate form upon initial request, if the form is valid save it in the
datebase and finally dispatch the user to the set success url.

Classes:
    AgeGate

Functions:
    n/a

Created on 05 Mar 2013

@author: michael

"""
from django.views import generic as generic_views
from django.http import HttpResponseRedirect

class AgeGate(generic_views.FormView):
    """
    View the user gets sent to when an Age Gate
    is encountered.

    """

    def get_initial(self):
        """The initial view is defaulted to next."""
        return {'next': self.request.GET.get('next')}

    def get_success_url(self):
        """The success url is set to the home page."""
        return self.request.POST.get('next') or '/'

    def form_valid(self, form):
        """If the form is valid, save it in the database."""
        form.save(self.request)

        return HttpResponseRedirect(self.get_success_url())

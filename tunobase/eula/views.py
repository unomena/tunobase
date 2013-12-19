"""
EULA APP

This module provides an interface for the user to interact with
the EULA.

Classes:
    SignEULA
    SignEULAObject

Functions:
    n/a

Created on 23 Oct 2013

@author: michael

"""
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic as generic_views

from tunobase.eula import models

class SignEULA(generic_views.FormView):
    """Display EULA form to the user."""

    def get_form_kwargs(self):
        """Fetch the latest EULA."""

        kwargs = super(SignEULA, self).get_form_kwargs()

        kwargs.update({
            'eula': get_object_or_404(models.EULA).latest_version(),
        })

        return kwargs

    def get_initial(self):
        """Set the next page to go to link."""

        return {'next': self.request.GET.get('next')}

    def get_success_url(self):
        """Upon success redirect to 'next' or home page."""

        return self.request.POST.get('next') or '/'

    def form_valid(self, form):
        """
        Upon validation, save the form and redirect to
        success url.

        """
        try:
            form.save(self.request)
        except IntegrityError:
            pass

        return HttpResponseRedirect(self.get_success_url())


class SignEULAObject(SignEULA):
    """Update form parameters with content_type_id and object_pk."""

    def get_form_kwargs(self):
        """Update form parameters with content_type_id and object_pk."""

        kwargs = super(SignEULAObject, self).get_form_kwargs()

        kwargs.update({
            'content_type_id': self.kwargs['content_type_id'],
            'object_pk': self.kwargs['object_pk']
        })

        return kwargs


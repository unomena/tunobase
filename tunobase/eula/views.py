'''
Created on 23 Oct 2013

@author: michael
'''
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic as generic_views

from tunobase.eula import models

class SignEULA(generic_views.FormView):

    def get_form_kwargs(self):
        kwargs = super(SignEULA, self).get_form_kwargs()

        kwargs.update({
            'eula': get_object_or_404(models.EULA).latest_version(),
        })

        return kwargs

    def get_initial(self):
        return {'next': self.request.GET.get('next')}

    def get_success_url(self):
        return self.request.POST.get('next') or '/'

    def form_valid(self, form):
        try:
            form.save(self.request)
        except IntegrityError:
            pass

        return HttpResponseRedirect(self.get_success_url())


class SignEULAObject(SignEULA):

    def get_form_kwargs(self):
        kwargs = super(SignEULAObject, self).get_form_kwargs()

        kwargs.update({
            'content_type_id': self.kwargs['content_type_id'],
            'object_pk': self.kwargs['object_pk']
        })

        return kwargs


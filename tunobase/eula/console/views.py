"""
EULA CONSOLE APP

This module provides an interface for the user to
interact with EULAs.

Classes:
    AdminMixin
    EULAVersionFormSetMixin
    EULACreate
    EULAUpdate
    EULADetail
    EULADelete
    EULAList

Functions:
    n/a

Created on 05 Mar 2013

@author: michael

"""
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic as generic_views

from tunobase.core import mixins as core_mixins
from tunobase.console import mixins as console_mixins
from tunobase.eula import models as eula_models
from tunobase.eula.console import forms

class AdminMixin(console_mixins.ConsoleUserRequiredMixin,
        core_mixins.PermissionRequiredMixin):
    """Only allow console users to acces this method."""

    raise_exception = False


class EULAVersionFormSetMixin(object):

    def get_context_data(self, **kwargs):
        """Set up empty form depending on request method."""

        context = super(EULAVersionFormSetMixin, self)\
                .get_context_data(**kwargs)

        if self.request.method == 'POST':
            context['formset'] = forms.EULAVersionFormSet(
                    self.request.POST, self.request.FILES,
                    instance=self.object
            )
        else:
            context['formset'] = forms.EULAVersionFormSet(
                    instance=self.object
            )

        return context

    def form_valid(self, form):
        """Upon validation save form in the database."""

        context = self.get_context_data()

        formset = context['formset']

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return HttpResponseRedirect(self.get_success_url())

        return self.render_to_response(self.get_context_data(form=form))


class EULACreate(AdminMixin, EULAVersionFormSetMixin,
        generic_views.CreateView):
    """Only allow users with console access to create EULAS."""

    permission_required = 'eula.add_eula'

    def get_success_url(self):
        """Set success url."""

        return reverse('console_eula_detail', args=(self.object.pk,))


class EULAUpdate(AdminMixin, EULAVersionFormSetMixin,
        generic_views.UpdateView):
    """Only allow users with console access to update EULAs."""

    permission_required = 'eula.change_eula'

    def get_success_url(self):
        """Set success url."""

        return reverse('console_eula_detail', args=(self.object.pk,))

    def get_queryset(self):
        """Return a list of all saved EULAs."""

        return eula_models.EULA.objects.all()


class EULADetail(AdminMixin, generic_views.DetailView):
    """Only allow users with console access to view EULA details."""

    permission_required = 'eula.change_eula'

    def get_object(self):
        """Return detail description of EULA."""

        return get_object_or_404(eula_models.EULA, pk=self.kwargs['pk'])


class EULADelete(AdminMixin, generic_views.DeleteView):
    """Only allow users with console access to delete EULA details."""
    permission_required = 'eula.delete_eula'

    def get_success_url(self):
        """Set success url."""

        return reverse('console_eula_list')

    def get_queryset(self):
        """Return list of all saved EULAs."""

        return eula_models.EULA.objects.all()


class EULAList(AdminMixin, generic_views.ListView):
    """Only allow users with console access to view a list EULAs."""
    permission_required = 'eula.change_eula'

    def get_queryset(self):
        """Return a list of all EULAs."""

        return eula_models.EULA.objects.all()

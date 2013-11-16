'''
Created on 05 Mar 2013

@author: michael
'''
from django.views import generic as generic_views
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect

from tunobase.core import mixins as core_mixins
from tunobase.console import mixins as console_mixins
from tunobase.eula import models as eula_models
from tunobase.eula.console import forms

class AdminMixin(console_mixins.ConsoleUserRequiredMixin, core_mixins.PermissionRequiredMixin):
    raise_exception = False

class EULAVersionFormSetMixin(object):
    
    def get_context_data(self, **kwargs):
        context = super(EULAVersionFormSetMixin, self).get_context_data(**kwargs)
        
        if self.request.method == 'POST':
            context['formset'] = forms.EULAVersionFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = forms.EULAVersionFormSet(instance=self.object)
            
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        
        formset = context['formset']
        
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return HttpResponseRedirect(self.get_success_url())
        
        return self.render_to_response(self.get_context_data(form=form))
        
class EULACreate(AdminMixin, EULAVersionFormSetMixin, generic_views.CreateView):
    permission_required = 'eula.add_eula'
    
    def get_success_url(self):
        return reverse('console_eula_detail', args=(self.object.pk,))

class EULAUpdate(AdminMixin, EULAVersionFormSetMixin, generic_views.UpdateView):
    permission_required = 'eula.change_eula'
    
    def get_success_url(self):
        return reverse('console_eula_detail', args=(self.object.pk,))

    def get_queryset(self):
        return eula_models.EULA.objects.all()

class EULADetail(AdminMixin, generic_views.DetailView):
    permission_required = 'eula.change_eula'

    def get_object(self):
        return get_object_or_404(eula_models.EULA, pk=self.kwargs['pk'])

class EULADelete(AdminMixin, generic_views.DeleteView):
    permission_required = 'eula.delete_eula'
    
    def get_success_url(self):
        return reverse('console_eula_list')

    def get_queryset(self):
        return eula_models.EULA.objects.all()

class EULAList(AdminMixin, generic_views.ListView):
    permission_required = 'eula.change_eula'
    
    def get_queryset(self):
        return eula_models.EULA.objects.all()
    
    
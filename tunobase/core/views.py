'''
Created on 23 Oct 2013

@author: michael
'''
from django.views import generic as generic_views
from django.http import Http404, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.shortcuts import get_object_or_404

from tunobase.core import models, utils, mixins

class ListWithDetailView(generic_views.ListView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})
        context = self.get_context_data(object=self.object,
            object_list=self.object_list,
            request=self.request)
        return self.render_to_response(context)
    
class MarkDeleteView(generic_views.DeleteView):
    
    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.mark_deleted()
        return HttpResponseRedirect(success_url)
    
class ContentBlockUpdate(mixins.AdminRequiredMixin, generic_views.View):
    
    def post(self, request, *args, **kwargs):
        slug = request.POST.get('slug')
        content = request.POST.get('content')
        
        content_block = get_object_or_404(models.ContentModel, slug=slug)
        content_block.content = content
        content_block.save()
        
        return utils.respond_with_json({'success': True})
'''
Created on 29 Oct 2013

@author: michael
'''
from django.views import generic as generic_views
from django.template.loader import render_to_string

from tunobase.core import utils as core_utils
from tunobase.tagging import models

class RetrieveTags(generic_views.View):
    
    def get(self, request, *args, **kwargs):
        term = request.GET.get('term', '')
        
        return core_utils.respond_with_json(
            [tag.title for tag in models.Tag.objects.for_current_site().filter(
                title__icontains=term)
            ]
        )
class UpdateTags(generic_views.FormView):
    
    def form_valid(self, form):
        form.save(self.request.POST.getlist('tags', []))
        
        return core_utils.respond_with_json({
            'success': True
        })
        
    def form_invalid(self, form):
        return core_utils.respond_with_json({
            'success': False
        })
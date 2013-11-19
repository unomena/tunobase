'''
Created on 29 Oct 2013

@author: michael
'''
from django.views import generic as generic_views
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib import messages
from django.shortcuts import redirect

from tunobase.core import utils as core_utils, mixins as core_mixins
from tunobase.commenting import models, exceptions

class PostComment(generic_views.FormView):
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        if form.is_valid():
            return self.ajax_form_valid(form) \
                if request.is_ajax() else self.form_valid(form)
        else:
            return self.ajax_form_invalid(form) \
                if request.is_ajax() else self.form_invalid(form)
        
    def form_valid(self, form):
        try:
            form.save(self.request)
            messages.success(self.request, 'Your comment has been posted')
        except exceptions.RapidCommentingError as e:
            messages.error(self.request, e)
            
        return redirect(self.request.META['HTTP_REFERER'])
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        
        return redirect(self.request.META['HTTP_REFERER'])
    
    def ajax_form_valid(self, form):
        try:
            comment = form.save(self.request)
            num_comments = models.CommentModel.objects.permitted().count()
            
            return core_utils.respond_with_json({
                'success': True,
                'comment': render_to_string(
                    self.template_name, 
                    RequestContext(self.request, {'comment': comment})
                ),
                'num_comments': num_comments
            })
        except exceptions.RapidCommentingError as e:
            return core_utils.respond_with_json({
                'success': False,
                'reason': e.value
            })
        
    def ajax_form_invalid(self, form):
        return core_utils.respond_with_json({
            'success': False,
            'reason': str(form.errors)
        })
        
class LoadMoreComments(core_mixins.AjaxMorePaginationMixin, generic_views.ListView):
    
    def get_queryset(self):
        return models.CommentModel.objects.permitted().get_comments_for_object(
            self.request.GET['content_type_id'],
            self.request.GET['object_pk'],
        )
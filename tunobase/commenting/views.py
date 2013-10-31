'''
Created on 29 Oct 2013

@author: michael
'''
from django.views import generic as generic_views
from django.template import RequestContext
from django.template.loader import render_to_string

from tunobase.core import utils as core_utils, mixins as core_mixins
from tunobase.commenting import models, exceptions

class PostComment(generic_views.FormView):
    
    def form_valid(self, form):
        try:
            comment = form.save(self.request)
            num_comments = models.CommentModel.permitted.count()
            
            return core_utils.respond_with_json({
                'success': True,
                'comment': render_to_string(
                    'commenting/includes/comment.html', 
                    RequestContext(self.request, {'comment': comment})
                ),
                'num_comments': num_comments
            })
        except exceptions.RapidCommentingError as e:
            return core_utils.respond_with_json({
                'success': False,
                'reason': e.value
            })
        
    def form_invalid(self, form):
        return core_utils.respond_with_json({
            'success': False,
            'reason': str(form.errors)
        })
        
class LoadMoreComments(core_mixins.AjaxMorePaginationMixin, generic_views.ListView):
    
    def get_queryset(self):
        return models.CommentModel.permitted.get_comments_for_object(
            self.request.GET['content_type_id'],
            self.request.GET['object_pk'],
        )
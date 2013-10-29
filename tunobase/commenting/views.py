'''
Created on 29 Oct 2013

@author: michael
'''
from django.views import generic as generic_views
from django.template.loader import render_to_string

from tunobase.core import utils as core_utils
from tunobase.commenting import models

class PostComment(generic_views.FormView):
    
    def get_form_kwargs(self):
        kwargs = super(PostComment, self).get_form_kwargs()
        
        if self.request.user.is_authenticated():
            kwargs.update({'user': self.request.user})
            
        return kwargs
    
    def form_valid(self, form):
        comment = form.save()
        
        num_comments = models.CommentModel.permitted.count()
        
        return core_utils.respond_with_json({
            'success': True,
            'comment': render_to_string(
                'commenting/includes/comment.html', 
                {'comment': comment}
            ),
            'num_comments': num_comments
        })
        
    def form_invalid(self, form):
        return core_utils.respond_with_json({
            'success': False
        })
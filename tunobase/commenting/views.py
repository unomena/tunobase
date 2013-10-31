'''
Created on 29 Oct 2013

@author: michael
'''
from django.views import generic as generic_views
from django.template.loader import render_to_string

from tunobase.core import utils as core_utils
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
                    {'comment': comment}
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
            'success': False
        })
        
class LoadMoreComments(generic_views.FormView):
    
    def get_form_kwargs(self):
        '''
        Returns the keyword arguments for instantiating the form.
        '''
        kwargs = {'initial': self.get_initial()}
        if self.request.method == 'GET':
            kwargs.update({
                'data': self.request.GET
            })
            
        return kwargs
    
    def get(self, request, *args, **kwargs):
        '''
        Handles GET requests.
        '''
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    
    def form_valid(self, form):
        comments, _ = form.retrieve()
        
        return core_utils.respond_with_json({
            'success': True,
            'comments': render_to_string(
                'commenting/includes/comments.html', {
                   'comments': comments,
                   'content_type_id': form.cleaned_data['comment_content_type_id'],
                   'object_pk': form.cleaned_data['comment_object_pk'],
                   'paginate_by': form.cleaned_data['paginate_by']
                }
            )
        })
        
    def form_invalid(self, form):
        return core_utils.respond_with_json({
            'success': False
        })
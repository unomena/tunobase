'''
Created on 25 Oct 2013

@author: michael
'''
from django.conf.urls.defaults import patterns, url

from tunobase.commenting import views, forms

urlpatterns = patterns('',            
    url(r'^post-comment/$',
        views.PostComment.as_view(
            form_class=forms.CommentForm
        ),
        name='post_comment'
    ),
                       
    url(r'^load-more-comments/$',
        views.LoadMoreComments.as_view(
            form_class=forms.LoadCommentsForm
        ),
        name='load_more_comments'
    ),
)

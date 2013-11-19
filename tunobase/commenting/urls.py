'''
Created on 25 Oct 2013

@author: michael
'''
from django.conf.urls import patterns, url

from honeypot.decorators import check_honeypot

from tunobase.commenting import views, forms

urlpatterns = patterns('',
                              
    url(r'^post-comment/$',
        check_honeypot(views.PostComment.as_view(
            form_class=forms.CommentForm,
            template_name='commenting/includes/comment.html'
        )),
        name='post_comment'
    ),
                       
    url(r'^load-more-comments/$',
        views.LoadMoreComments.as_view(
            partial_template_name='commenting/includes/comments.html'
        ),
        name='load_more_comments'
    ),
)

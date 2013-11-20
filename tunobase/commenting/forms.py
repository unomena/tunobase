'''
Created on 29 Oct 2013

@author: michael
'''
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.utils import timezone
from django.conf import settings

from tunobase.core import utils as core_utils, throttling as core_throttling
from tunobase.commenting import models, exceptions, throttling

class CommentForm(forms.Form):
    user_id = forms.IntegerField(required=False)
    user_name = forms.CharField(max_length=100, required=False)
    comment_content_type_id = forms.IntegerField()
    comment_object_pk = forms.CharField()
    comment_box = forms.CharField(max_length=512)
    
    def save(self, request):
        ip_address = core_utils.get_client_ip(request)
        comment_period_lockout = getattr(settings, 'COMMENT_PERIOD_LOCKOUT', None)
        num_comments_allowed_in_lockout = \
            getattr(settings, 'NUM_COMMENTS_ALLOWED_IN_PERIOD', 5)
        throttle_key = 'commenting'
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None
        
        if comment_period_lockout is not None:
            if core_throttling.check_throttle_exists(request, throttle_key):
                throttled = not core_throttling.check_throttle(
                    request, 
                    throttle_key, 
                    comment_period_lockout, 
                    num_comments_allowed_in_lockout
                )
            else:
                throttled = not throttling.check_throttle(
                    user, 
                    ip_address, 
                    comment_period_lockout, 
                    num_comments_allowed_in_lockout
                )
                
            if throttled:
                raise exceptions.RapidCommentingError(
                    "You are commenting too quickly. "
                    "Please wait before commenting again"
                )
        
        comment = models.CommentModel.objects.create(
            user=user,
            created_by=user,
            modified_by=user,
            user_name=self.cleaned_data['user_name'],
            ip_address=ip_address,
            site=Site.objects.get_current(),
            content_type_id=self.cleaned_data['comment_content_type_id'],
            object_pk=self.cleaned_data['comment_object_pk'],
            comment=self.cleaned_data['comment_box']
        )
        
        core_throttling.add_to_throttle(request, throttle_key, comment.publish_at)
        
        return comment
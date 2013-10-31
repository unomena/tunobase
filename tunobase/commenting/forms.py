'''
Created on 29 Oct 2013

@author: michael
'''
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.paginator import Paginator
from django.utils import timezone
from django.conf import settings

from tunobase.core import utils as core_utils
from tunobase.commenting import models, exceptions

class CommentForm(forms.Form):
    user_id = forms.IntegerField(required=False)
    user_name = forms.CharField(max_length=100, required=False)
    comment_content_type_id = forms.IntegerField()
    comment_object_pk = forms.CharField()
    comment_box = forms.CharField(max_length=512)
    
    def save(self, request):
        ip_address = core_utils.get_client_ip(request)
        comment_delay_minutes = getattr(settings, 'COMMENT_DELAY_MINUTES', 0)
        comment_delay_seconds = getattr(settings, 'COMMENT_DELAY_SECONDS', 0)
        
        if comment_delay_minutes or comment_delay_seconds:
            latest_comment_list = list(
                models.CommentModel.objects.filter(
                    ip_address=ip_address).order_by('-publish_at'
                )[:5]
            )
            if len(latest_comment_list) == 5:
                latest_comment = latest_comment_list[-1]
                if latest_comment.publish_at > timezone.now() - \
                   timezone.timedelta(
                       minutes=comment_delay_minutes, 
                       seconds=comment_delay_seconds
                    ):
                    raise exceptions.RapidCommentingError(
                        "You are commenting too quickly. "
                        "Please wait before commenting again"
                    )
        
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None
        
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
        
        return comment
    
class LoadCommentsForm(forms.Form):
    comment_content_type_id = forms.IntegerField()
    comment_object_pk = forms.CharField()
    page = forms.IntegerField()
    paginate_by = forms.IntegerField()
    
    def retrieve(self):
        comments = models.CommentModel.permitted.get_comments_for_object(
            self.cleaned_data['comment_content_type_id'],
            self.cleaned_data['comment_object_pk'],
            site=Site.objects.get_current()
        )
        
        paginator = Paginator(comments, self.cleaned_data['paginate_by'])
            
        return paginator.page(self.cleaned_data['page']), paginator.count
        
        
"""
Commenting App

This module provides the fields for the comment form.

"""
from django import forms
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from tunobase.core import utils as core_utils, throttling as core_throttling
from tunobase.commenting import models, exceptions, throttling


class CommentForm(forms.Form):
    """Set up the required fields for the comments form."""

    anonymous = forms.BooleanField(required=False)
    next = forms.CharField(required=False)
    user_id = forms.IntegerField(required=False)
    user_name = forms.CharField(max_length=100, required=False)
    comment_content_type_id = forms.IntegerField()
    comment_object_pk = forms.CharField()
    comment_box = forms.CharField(max_length=512)

    def save(self, request):
        """Process and save cleaned data in the database."""

        ip_address = core_utils.get_client_ip(request)
        comment_period_lockout = getattr(
                settings, 'COMMENT_PERIOD_LOCKOUT', None
        )
        num_comments_allowed_in_lockout = \
            getattr(settings, 'NUM_COMMENTS_ALLOWED_IN_PERIOD', 5)
        throttle_key = 'commenting_%s_%s' % (
            self.cleaned_data['comment_content_type_id'],
            self.cleaned_data['comment_object_pk']
        )
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None

        if comment_period_lockout is not None:
            if core_throttling.check_throttle_exists(request, throttle_key):
                throttled = core_throttling.check_throttle(
                    request,
                    throttle_key,
                    comment_period_lockout,
                    num_comments_allowed_in_lockout
                )
            else:
                throttled = throttling.check_throttle(
                    user,
                    ip_address,
                    comment_period_lockout,
                    num_comments_allowed_in_lockout
                )

            if throttled:
                raise exceptions.RapidCommentingError(
                    _("You are commenting too quickly. "
                    "Please wait before commenting again")
                )

        if self.cleaned_data['anonymous']:
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

        core_throttling.add_to_throttle(
            request, throttle_key, comment.publish_at
        )

        return comment

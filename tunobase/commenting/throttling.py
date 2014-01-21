"""
Commenting App

This module prevent users from commenting overzealously.

"""
from django.utils import timezone

from tunobase.commenting import models


def check_throttle(user, ip_address, comment_period_lockout,
                   num_comments_allowed_in_lockout):
    """Prevent users from posting comments overzealously."""

    if user is not None:
        queryset = models.CommentModel.objects.filter(
            user=user
        )
    else:
        queryset = models.CommentModel.objects.filter(
            ip_address=ip_address
        )

    latest_comment_list = list(
        queryset.order_by('-publish_at')[:num_comments_allowed_in_lockout]
    )
    if len(latest_comment_list) == num_comments_allowed_in_lockout:
        oldest_comment = latest_comment_list[-1]
        return oldest_comment.publish_at > (
           timezone.now() - comment_period_lockout
        )

    return False

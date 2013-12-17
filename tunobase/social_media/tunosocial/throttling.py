'''
Created on 20 Nov 2013

@author: michael
'''
from django.utils import timezone

from tunobase.social_media.tunosocial import models

def check_throttle(user, ip_address, like_period_lockout,
        num_likes_allowed_in_lockout):
    if user is not None:
        queryset = models.Like.objects.filter(
            user=user
        )
    else:
        queryset = models.Like.objects.filter(
            ip_address=ip_address
        )

    latest_like_list = list(
        queryset.order_by('-created_at')[:num_likes_allowed_in_lockout]
    )
    if len(latest_like_list) == num_likes_allowed_in_lockout:
        oldest_like = latest_like_list[-1]
        return oldest_like.created_at > (timezone.now() - like_period_lockout)

    return False

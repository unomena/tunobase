'''
Created on 29 Oct 2013

@author: michael
'''
from django.views import generic as generic_views
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils import timezone

from tunobase.core import utils as core_utils, throttling as core_throttling
from tunobase.social_media.tunosocial import models, exceptions

class AddLike(generic_views.View):
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None
        content_type_id = request.POST.get('content_type_id', None)
        object_pk = request.POST.get('object_pk', None)
        ip_address = core_utils.get_client_ip(request)
        like_period_lockout = getattr(settings, 'LIKE_PERIOD_LOCKOUT', None)
        num_likes_allowed_in_lockout = \
            getattr(settings, 'NUM_LIKES_ALLOWED_IN_PERIOD', 5)
        throttle_key = 'liking_%s' % object_pk
        
        if like_period_lockout is not None:
            if core_throttling.check_throttle_exists(request, throttle_key):
                throttled = not core_throttling.check_throttle(
                    request, 
                    throttle_key, 
                    like_period_lockout, 
                    num_likes_allowed_in_lockout
                )
            else:
                latest_like_list = list(
                    models.Like.objects.filter(
                        ip_address=ip_address
                    ).order_by('-created_at')[:num_likes_allowed_in_lockout]
                )
                if len(latest_like_list) == num_likes_allowed_in_lockout:
                    oldest_like = latest_like_list[-1]
                    throttled = oldest_like.created_at > timezone.now() - like_period_lockout
                else:
                    throttled = False
                
            if throttled:
                return core_utils.respond_with_json({
                    'success': False,
                    'reason': 'You are liking too quickly. '
                        'Please wait before liking again'
                })
        
        like = models.Like.objects.create(
            user=user,
            content_type_id=content_type_id,
            object_pk=object_pk,
            site=Site.objects.get_current(),
            ip_address=ip_address
        )
        
        core_throttling.add_to_throttle(request, throttle_key, like.created_at)
        
        return core_utils.respond_with_json({
            'success': True
        })
        
class RemoveLike(generic_views.View):
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None
        content_type_id = request.POST.get('content_type_id', None)
        object_pk = request.POST.get('object_pk', None)
        ip_address = core_utils.get_client_ip(request)
        like_period_lockout = getattr(settings, 'LIKE_PERIOD_LOCKOUT', None)
        num_likes_allowed_in_lockout = \
            getattr(settings, 'NUM_LIKES_ALLOWED_IN_PERIOD', 5)
        throttle_key = 'liking_%s' % object_pk
        
        if like_period_lockout is not None:
            if core_throttling.check_throttle_exists(request, throttle_key):
                throttled = not core_throttling.check_throttle(
                    request, 
                    throttle_key, 
                    like_period_lockout, 
                    num_likes_allowed_in_lockout
                )
            else:
                latest_like_list = list(
                    models.Like.objects.filter(
                        ip_address=ip_address
                    ).order_by('-created_at')[:num_likes_allowed_in_lockout]
                )
                if len(latest_like_list) == num_likes_allowed_in_lockout:
                    oldest_like = latest_like_list[-1]
                    throttled = oldest_like.created_at > timezone.now() - like_period_lockout
                else:
                    throttled = False
                
            if throttled:
                return core_utils.respond_with_json({
                    'success': False,
                    'reason': 'You are liking too quickly. '
                        'Please wait before liking again'
                })
        
        like = get_object_or_404(
            models.Like, 
            user=user,
            content_type_id=content_type_id,
            object_pk=object_pk
        )
        like.delete()
        
        return core_utils.respond_with_json({
            'success': True
        })
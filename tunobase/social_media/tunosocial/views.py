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
from django.shortcuts import redirect
from django.contrib import messages

from tunobase.core import utils as core_utils, throttling as core_throttling
from tunobase.social_media.tunosocial import models, exceptions, throttling

def validate(self, user, throttle_key, ip_address):
    like_period_lockout = getattr(settings, 'LIKE_PERIOD_LOCKOUT', None)
    num_likes_allowed_in_lockout = \
        getattr(settings, 'NUM_LIKES_ALLOWED_IN_PERIOD', 5)
    if like_period_lockout is not None:
        if core_throttling.check_throttle_exists(self.request, throttle_key):
            throttled = not core_throttling.check_throttle(
                self.request, 
                throttle_key, 
                like_period_lockout, 
                num_likes_allowed_in_lockout
            )
        else:
            throttled = not throttling.check_throttle(
                user, 
                ip_address, 
                like_period_lockout, 
                num_likes_allowed_in_lockout
            )
            
        if throttled:
            raise exceptions.RapidLikingError(
                'You are liking too quickly. '
                'Please wait before liking again'
            )

class AddLike(generic_views.View):
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None
        content_type_id = request.POST.get('content_type_id', None)
        object_pk = request.POST.get('object_pk', None)
        ip_address = core_utils.get_client_ip(request)
        throttle_key = 'liking_%s' % object_pk
        
        try:
            self.validate(user, throttle_key, ip_address)
        except exceptions.RapidLikingError, e:
            if request.is_ajax():
                return core_utils.respond_with_json({
                    'success': False,
                    'reason': e
                })
                
            messages.error(request, e)
            return redirect(request.META['HTTP_REFERER'])
        
        like = models.Like.objects.create(
            user=user,
            content_type_id=content_type_id,
            object_pk=object_pk,
            site=Site.objects.get_current(),
            ip_address=ip_address
        )
        
        core_throttling.add_to_throttle(request, throttle_key, like.created_at)
        
        if request.is_ajax():
            return core_utils.respond_with_json({
                'success': True
            })
        
        messages.success(request, 'You have liked this')
        return redirect(request.META['HTTP_REFERER'])
        
class RemoveLike(generic_views.View):

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None
        content_type_id = request.POST.get('content_type_id', None)
        object_pk = request.POST.get('object_pk', None)
        ip_address = core_utils.get_client_ip(request)
        throttle_key = 'liking_%s' % object_pk
        
        try:
            self.validate(user, throttle_key, ip_address)
        except exceptions.RapidLikingError, e:
            if request.is_ajax():
                return core_utils.respond_with_json({
                    'success': False,
                    'reason': e
                })
            
            messages.error(request, e)
            return redirect(request.META['HTTP_REFERER'])
        
        like = get_object_or_404(
            models.Like, 
            user=user,
            content_type_id=content_type_id,
            object_pk=object_pk
        )
        like.delete()
        
        if request.is_ajax():
            return core_utils.respond_with_json({
                'success': True
            })
        
        messages.success(request, 'You have liked this')
        return redirect(request.META['HTTP_REFERER'])
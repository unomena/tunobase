'''
Created on 29 Oct 2013

@author: michael
'''
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404, redirect
from django.views import generic as generic_views

from tunobase.core import (
    utils as core_utils,
    throttling as core_throttling,
    mixins as core_mixins
)
from tunobase.social_media.tunosocial import models, exceptions, throttling

def _validate(request, user, throttle_key, ip_address, action):
    already_liked = request.COOKIES.get(throttle_key, None)
    if user is None and already_liked is None and action == 'remove':
        raise exceptions.UnauthorizedLikingError(
            "This is not yours"
        )

    if user is None and already_liked and action == 'add':
        raise exceptions.UnauthorizedLikingError(
            "You already like this"
        )

    like_period_lockout = getattr(settings, 'LIKE_PERIOD_LOCKOUT', None)
    num_likes_allowed_in_lockout = \
        getattr(settings, 'NUM_LIKES_ALLOWED_IN_PERIOD', 5)
    if like_period_lockout is not None:
        if core_throttling.check_throttle_exists(request, throttle_key):
            throttled = core_throttling.check_throttle(
                request,
                throttle_key,
                like_period_lockout,
                num_likes_allowed_in_lockout
            )
        else:
            throttled = throttling.check_throttle(
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

def _like(request, action):
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None

    if request.method == 'POST':
        content_type_id = request.POST.get('content_type_id', None)
        object_pk = request.POST.get('object_pk', None)
    else:
        content_type_id = request.GET.get('content_type_id', None)
        object_pk = request.GET.get('object_pk', None)

    ip_address = core_utils.get_client_ip(request)
    throttle_key = 'liking_%s_%s' % (content_type_id, object_pk)

    _validate(request, user, throttle_key, ip_address, action)

    if action == 'add':
        like = models.Like.objects.create(
            user=user,
            content_type_id=content_type_id,
            object_pk=object_pk,
            site=Site.objects.get_current(),
            ip_address=ip_address
        )

        core_throttling.add_to_throttle(request, throttle_key, like.created_at)
    elif action =='remove':
        like = get_object_or_404(
            models.Like,
            user=user,
            content_type_id=content_type_id,
            object_pk=object_pk
        )
        like.delete()

    return throttle_key


class AddLike(core_mixins.DeterministicLoginRequiredMixin,
        generic_views.View):

    def deterministic_function(self):
        return settings.ANONYMOUS_LIKES_ALLOWED

    def get(self, request, *args, **kwargs):
        try:
            throttle_key = _like(request, 'add')
        except (exceptions.RapidLikingError,
                exceptions.UnauthorizedLikingError), e:
            messages.error(request, e)
            redirect(request.META['HTTP_REFERER'])

        messages.success(request, 'You have liked this')
        response = redirect(request.META['HTTP_REFERER'])
        response.set_cookie(throttle_key, True)
        return response

    def post(self, request, *args, **kwargs):
        try:
            throttle_key = _like(request, 'add')
        except (exceptions.RapidLikingError,
                exceptions.UnauthorizedLikingError), e:
            return core_utils.respond_with_json({
                'success': False,
                'reason': str(e)
            })

        response = core_utils.respond_with_json({
            'success': True
        })
        response.set_cookie(throttle_key, True)
        return response


class RemoveLike(core_mixins.DeterministicLoginRequiredMixin,
        generic_views.View):

    def deterministic_function(self):
        return settings.ANONYMOUS_LIKES_ALLOWED

    def get(self, request, *args, **kwargs):
        try:
            throttle_key = _like(request, 'remove')
        except (exceptions.RapidLikingError,
                exceptions.UnauthorizedLikingError), e:
            messages.error(request, e)
            return redirect(request.META['HTTP_REFERER'])

        messages.success(request, 'You have unliked this')
        response = redirect(request.META['HTTP_REFERER'])
        response.delete_cookie(throttle_key)
        return response

    def post(self, request, *args, **kwargs):
        try:
            throttle_key = _like(request, 'remove')
        except (exceptions.RapidLikingError,
                exceptions.UnauthorizedLikingError), e:
            return core_utils.respond_with_json({
                'success': False,
                'reason': str(e)
            })

        response = core_utils.respond_with_json({
            'success': True
        })
        response.delete_cookie(throttle_key)
        return response

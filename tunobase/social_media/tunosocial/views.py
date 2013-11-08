'''
Created on 29 Oct 2013

@author: michael
'''
from django.views import generic as generic_views
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

from tunobase.core import utils as core_utils
from tunobase.social_media.tunosocial import models

class AddLike(generic_views.View):
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None
        content_type_id = request.POST.get('content_type_id', None)
        object_pk = request.POST.get('object_pk', None)
        
        like = models.Like.objects.create(
            user=user,
            content_type_id=content_type_id,
            object_pk=object_pk
        )
        
        return core_utils.respond_with_json({
            'success': True
        })
        
class RemoveLike(generic_views.View):
    
    def post(self, request, *args, **kwargs):
        content_type_id = request.POST.get('content_type_id', None)
        object_pk = request.POST.get('object_pk', None)
        
        like = get_object_or_404(
            models.Like, 
            content_type_id=content_type_id,
            object_pk=object_pk
        )
        like.delete()
        
        return core_utils.respond_with_json({
            'success': True
        })
'''
Created on 28 Oct 2013

@author: michael
'''
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.sites.models import Site

from tunobase.core import utils as core_utils

class LikeManager(models.Manager):
    
    def get_num_likes_for_object(self, obj, site=None):
        if site is None:
            site = Site.objects.get_current()
        
        return self.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_pk=obj.pk,
            site=site
        ).count()
            
    def get_already_liked(self, request, obj, site=None):
        if site is None:
            site = Site.objects.get_current()
            
        queryset = self.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_pk=obj.pk,
            site=site
        )
        
        if request.user.is_authenticated():
            return queryset.filter(
                user=request.user
            ).exists()
                
        return queryset.filter(
            ip_address=core_utils.get_client_ip(request)
        ).exists()
'''
Created on 28 Oct 2013

@author: michael
'''
from django.contrib.contenttypes.models import ContentType
from django.db import models

class LikeManager(models.Manager):
    
    def get_num_likes_for_object(self, obj, site=None):
        return super(LikeManager, self).get_query_set()\
            .filter(
                content_type=ContentType.objects.get_for_model(obj),
                object_pk=obj.pk,
                site=site
            ).count()
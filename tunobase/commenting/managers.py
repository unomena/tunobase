'''
Created on 28 Oct 2013

@author: michael
'''
from django.contrib.comments import managers as comment_managers
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings

from tunobase.core import managers as core_managers
from tunobase.commenting import query, constants

class CommentManager(core_managers.CoreStateManager, comment_managers.CommentManager):
    
    def get_queryset(self):
        return query.CommentQuerySet(self.model, using=self._db)
    
    def get_comments_for_object(self, content_type_id, object_pk, site=None):
        return self.get_queryset().get_comments_for_object(
            content_type_id,
            object_pk,
            site
        )
    
    def remove_flagged_comments(self):
        for comment in self.permitted():
            num_removal_flags = comment.flags.filter(
                flag=constants.FLAG_SUGGEST_REMOVAL
            ).count()
            if num_removal_flags >= getattr(settings, 'COMMENT_FLAGS_FOR_REMOVAL', 5):
                comment.is_removed = True
                comment.save()
        
class CommentFlagManager(models.Manager):
    
    def report(self, user, comment_id):
        self.create(
            user=user, 
            comment_id=comment_id,
            flag=constants.FLAG_SUGGEST_REMOVAL
        )
        
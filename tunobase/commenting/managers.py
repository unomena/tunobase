'''
Created on 28 Oct 2013

@author: michael
'''
from django.contrib.comments import managers as comment_managers
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from tunobase.core import managers as core_managers
from tunobase.commenting import query

class CommentManager(core_managers.CoreStateManager, comment_managers.CommentManager):
    
    def get_queryset(self):
        return query.CommentQuerySet(self.model, using=self._db)
    
    def get_comments_for_object(self, content_type_id, object_pk, site=None):
        return self.get_queryset().get_comments_for_object(
            content_type_id,
            object_pk,
            site
        )
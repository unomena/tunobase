'''
Created on 28 Oct 2013

@author: michael
'''
from django.contrib.comments import managers as comment_managers
from django.contrib.contenttypes.models import ContentType

from tunobase.core import managers as core_managers

class CommentManager(core_managers.StateManagerMixin, comment_managers.CommentManager):
    
    def get_comments_for_object(self, obj, site=None):
        return super(CommentManager, self).get_query_set().filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_pk=obj.pk,
            site=site
        )
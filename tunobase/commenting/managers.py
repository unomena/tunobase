'''
Created on 28 Oct 2013

@author: michael
'''
from django.contrib.comments import managers as comment_managers
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from tunobase.core import managers as core_managers

class CommentManager(core_managers.StateManagerMixin, comment_managers.CommentManager):
    
    def get_comments_for_object(self, content_type_id, object_pk, site=None):
        if site is None:
            site = Site.objects.get_current()
        
        return super(CommentManager, self).get_query_set().filter(
            content_type_id=content_type_id,
            object_pk=object_pk,
            site=site
        )
'''
Created on 25 Oct 2013

@author: michael
'''
from django.contrib.sites.models import Site

from tunobase.core import query as core_query
    
class CommentQuerySet(core_query.CoreStateQuerySet):
    
    def get_comments_for_object(self, content_type_id, object_pk, site=None):
        if site is None:
            site = Site.objects.get_current()
        
        return self.select_related('user').filter(
            content_type_id=content_type_id,
            object_pk=object_pk,
            site=site
        )
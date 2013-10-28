'''
Created on 28 Oct 2013

@author: michael
'''
from django.contrib.comments import managers as comment_managers
from django.contrib.contenttypes.models import ContentType
from django.db import models

from tunobase.core import managers as core_managers

class ContentObjectTagManager(models.Manager):
    
    def get_tags_for_object(self, model, pk, site=None):
        return super(ContentObjectTagManager, self).get_query_set().filter(
            content_type=ContentType.objects.get_for_model(model),
            object_pk=pk,
            site=site
        )
        
    def get_unique_tags_for_object(self, model, pk, site=None):
        return self.get_tags_for_object(model, pk, site).distinct()
    
    def get_tag_counts_for_object(self, model, pk, site=None):
        content_object_tags = self.get_tags_for_object(model, pk, site)
        tag_counter_dict = {}
        
        for content_object_tag in content_object_tags:
            title = content_object_tag.tag.title
            if title in tag_counter_dict:
                tag_counter_dict[title] += 1
            else:
                tag_counter_dict[title] = 1
                
        return tag_counter_dict

class TagManager(core_managers.StateManagerMixin):
    pass
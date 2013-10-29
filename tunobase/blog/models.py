'''
Created on 25 Oct 2013

@author: michael
'''
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

from tunobase.core import models as core_models, managers as core_managers

class Blog(core_models.ContentModel):
    '''
    Blogs the Site has
    '''
    default_manager = core_managers.SiteObjectsManager()

class BlogEntry(core_models.ContentModel):
    '''
    Entries per Blog
    '''
    blog = models.ForeignKey(Blog)
    author_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='blog_entries_authored', 
        null=True, 
        blank=True
    )
    authors_alternate = models.CharField(
        max_length=512, 
        blank=True, 
        null=True
    )
    
    default_manager = core_managers.SiteObjectsManager()

    class Meta:
        ordering = ['-publish_at']
        verbose_name_plural = 'Blog entries'
        
    def get_absolute_url(self):
        return reverse('blog_entry_detail', args=(self.slug,))
    
    @property
    def authors(self):
        '''
        Return a list of authors selected as users on the system and a list
        of alternate authors as not users on the system if either exist
        '''
        authors_dict = {}
        
        auth_users = self.author_users.all()
        if auth_users:
            authors_dict.update({
                'users': auth_users
            })
            
        if self.authors_alternate:
            authors_dict.update({
                'alternate': self.authors_alternate.split(',')
            })
        
        return authors_dict
            
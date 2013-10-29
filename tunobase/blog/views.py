'''
Created on 29 Oct 2013

@author: michael
'''
from django.http import Http404
from django.views import generic as generic_views
from django.contrib.syndication.views import Feed
from django.conf import settings
from django.utils.html import strip_tags

from tunobase.core import views as core_views, utils as core_utils, \
    constants as core_constants
from tunobase.tagging import models as tagging_models
from tunobase.blog import models

class BlogDetail(core_views.ListWithDetailView):

    def get_object(self):
        return core_utils.get_permitted_object_or_404(
            models.Blog, 
            slug=self.kwargs['slug']
        )

    def get_queryset(self):
        if 'tag' in self.request.GET:
            return tagging_models.ContentObjectTag.objects.filter(
                tag__title__iexact=self.request.GET['tag'],
                content_object__state__in=[
                    core_constants.STATE_STAGED, 
                    core_constants.STATE_PUBLISHED
                ],
                content_object__blog=self.object
            )
        
        return models.BlogEntry.permitted.filter(blog=self.object)

class SingleBlogDetail(BlogDetail):

    def get_object(self):
        blogs = models.Blog.permitted.all()
        if blogs:
            return blogs[0]
        
        raise Http404('No blogs available')

class BlogList(generic_views.ListView):

    def get_queryset(self):
        return models.Blog.permitted.all()

class BlogEntryDetail(generic_views.DetailView):

    def get_object(self):
        return core_utils.get_permitted_object_or_404(
            models.BlogEntry,
            slug=self.kwargs['slug']
        )
    
class BlogFeed(Feed):
    title = "%s Blog" % settings.APP_NAME
    link = "/blog/"
    description = "Blog entries for %s" % settings.APP_NAME

    def items(self):
        return models.BlogEntry.permitted.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return strip_tags(item.content)
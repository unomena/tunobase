'''
Created on 29 Oct 2013

@author: michael
'''
from django.http import Http404
from django.views import generic as generic_views
from django.contrib.syndication.views import Feed
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils.html import strip_tags

from tunobase.core import views as core_views, utils as core_utils, \
    constants as core_constants, mixins as core_mixins
from tunobase.tagging import models as tagging_models
from tunobase.blog import models

class BlogDetail(core_mixins.AjaxMorePaginationMixin, core_views.ListWithDetailView):

    def get_object(self):
        return core_utils.get_permitted_object_or_404(
            models.Blog, 
            slug=self.kwargs['slug']
        )

    def get_queryset(self):
        if 'tag' in self.request.GET:
            site = Site.objects.get_current()
            content_object_tags = tagging_models.ContentObjectTag.objects\
                .select_related('content_object').filter(
                    tag__title__iexact=self.request.GET['tag'],
                    content_type=ContentType.objects.get_for_model(models.BlogEntry),
                    site=site
                )
            
            blog_entries = []
            for content_object_tag in content_object_tags:
                if content_object_tag.content_object.state in [
                    core_constants.STATE_PUBLISHED, core_constants.STATE_STAGED
                   ]:
                    blog_entries.append(content_object_tag.content_object)
                    
            return blog_entries
        
        return models.BlogEntry.objects.permitted().filter(blog=self.object)

class SingleBlogDetail(BlogDetail):

    def get_object(self):
        blogs = models.Blog.objects.permitted()
        if blogs:
            return blogs[0]
        
        raise Http404('No blogs available')

class BlogList(generic_views.ListView):

    def get_queryset(self):
        return models.Blog.objects.permitted()

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
        return models.BlogEntry.objects.permitted()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return strip_tags(item.content)
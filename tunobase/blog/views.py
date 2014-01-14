"""
Blog App

This module retrieves and displays the list and detailed view of
blog posts.

Classes:
    BlogDetail
    SingleBlogDetail
    BlogList
    BlogEntryDetail
    BlogFeed

Functions:
    n/a

Created on 29 Oct 2013

@author: michael

"""
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.http import Http404
from django.utils.html import strip_tags
from django.views import generic as generic_views

from tunobase.blog import models
from tunobase.core import (
        views as core_views,
        utils as core_utils,
        constants as core_constants,
        mixins as core_mixins
)
from tunobase.tagging import models as tagging_models


class BlogDetail(core_mixins.AjaxMorePaginationMixin,
                 core_views.ListWithDetailView):
    """Return the detailed view of a blog post."""

    def get_object(self):
        """
        Return a particular blog post or throw a Not Found error
        should the post not exist.

        """
        return core_utils.get_permitted_object_or_404(
            models.Blog,
            slug=self.kwargs['slug']
        )

    def get_queryset(self):
        """
        Return posts relevant to selected tag else return
        relevant posts ensuring the are either of a published or
        staged state.

        """

        if 'tag' in self.request.GET:
            site = Site.objects.get_current()
            content_object_tags = tagging_models.ContentObjectTag.objects\
                .select_related('content_object').filter(
                    tag__title__iexact=self.request.GET['tag'],
                    content_type=ContentType.objects\
                            .get_for_model(models.BlogEntry),
                    site=site
                )

            blog_entries = []
            for content_object_tag in content_object_tags:
                if content_object_tag.content_object.state in [
                      core_constants.STATE_PUBLISHED,
                      core_constants.STATE_STAGED
                   ]:
                    blog_entries.append(content_object_tag.content_object)

            return blog_entries

        return models.BlogEntry.objects.permitted().filter(blog=self.object)


class SingleBlogDetail(BlogDetail):
    """Returns a single blog detail."""

    def get_object(self):
        """Returns a single blog object."""

        blogs = models.Blog.objects.permitted()
        if blogs:
            return blogs[0]

        raise Http404('No blogs available')


class BlogList(generic_views.ListView):
    """List view of all blogs."""

    def get_queryset(self):
        """Return all blog objects that are published."""

        return models.Blog.objects.permitted()


class BlogEntryDetail(generic_views.DetailView):
    """Provides a detailed view of a particular blog post."""

    def get_object(self):
        """Retrieve a blog post or throw a Not Found error."""

        return core_utils.get_permitted_object_or_404(
            models.BlogEntry,
            slug=self.kwargs['slug']
        )


class BlogFeed(Feed):
    """A blog feed."""

    title = "%s Blog" % settings.APP_NAME
    link = "/blog/"
    description = "Blog entries for %s" % settings.APP_NAME

    def items(self):
        """Returns all blog entries."""

        return models.BlogEntry.objects.permitted()

    def item_title(self, item):
        """Returns the titles of each post."""

        return item.title

    def item_description(self, item):
        """Returns the content of each post."""

        return strip_tags(item.rich_content)

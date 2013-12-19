"""
MEDIA APP

This module provides an interface for users to interact with events.

Classes:
    Articles
    ArticleDetail
    PressReleases
    PressReleaseDetail
    MediaCoverage
    Events

Functions:
    n/a

Created on 23 Oct 2013

@author: michael

"""
from django.views import generic as generic_views

from tunobase.core import utils as core_utils
from tunobase.corporate.media import models

class Articles(generic_views.ListView):
    """Return a list of articles."""

    def get_queryset(self):
        """Return a list of articles."""
        return models.Article.objects.permitted().for_current_site()


class ArticleDetail(generic_views.DetailView):
    """Return all information pertaining to a particular article."""

    def get_object(self):
        """Return article information."""

        return core_utils.get_permitted_object_for_current_site_or_404(
            models.Article,
            slug=self.kwargs['slug']
        )


class PressReleases(generic_views.ListView):
    """Return a list of all press releases."""

    def get_queryset(self):
        """Return a list of all press releases."""
        return models.PressRelease.objects.permitted().for_current_site()


class PressReleaseDetail(generic_views.DetailView):
    """Return all information on a particular press release."""

    def get_object(self):
        """Return all information on a particular press release."""
        return core_utils.get_permitted_object_for_current_site_or_404(
            models.PressRelease,
            slug=self.kwargs['slug']
        )


class MediaCoverage(generic_views.ListView):
    """Return a list of all media coverage articles."""

    def get_queryset(self):
        """Return a list of all media coverage articles."""
        return models.MediaCoverage.objects.permitted().for_current_site()


class Events(generic_views.TemplateView):
    """Return a list of all events."""

    def get_context_data(self, **kwargs):
        """Return a list of all events."""

        context = super(Events, self).get_context_data(**kwargs)

        context.update({
            'current_and_future_events': models.Event.objects\
                    .permitted()\
                    .current_and_future_events()\
                    .for_current_site(),
            'past_events': models.Event.objects\
                    .permitted()\
                    .past_events()\
                    .for_current_site(),
            'object_list': models.Event.objects\
                    .permitted()\
                    .for_current_site()
        })

        return context

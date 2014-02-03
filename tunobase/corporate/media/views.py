"""
MEDIA APP

This module provides an interface for users to interact with events.

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

        events = models.Event.objects.permitted().for_current_site()

        context.update({
            'current_and_future_events': events.current_and_future_events()\
                .order_by('start'),
            'past_events': events.past_events(),
            'object_list': events
                    
        })

        return context

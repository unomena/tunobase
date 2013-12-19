"""
MEDIA CONSOLE APP

This module provides an interface for users permitted
to access the console to be able to change media events.

Classes:
    AdminMixin
    MediaCoverageCreate
    MediaCoverageUpdate
    MediaCoverageDetail
    MediaCoverageDelete
    MediaCoverageList

Functions:
    n/a

Created on 05 Mar 2013

@author: michael

"""
from django.core.urlresolvers import reverse
from django.views import generic as generic_views

from tunobase.core import (
        mixins as core_mixins,
        utils as core_utils,
        views as core_views
)
from tunobase.console import mixins as console_mixins
from tunobase.corporate.media import models as media_models

class AdminMixin(console_mixins.ConsoleUserRequiredMixin,
        core_mixins.PermissionRequiredMixin):
    """Ensure user has rights to access the console."""

    raise_exception = False


class MediaCoverageCreate(AdminMixin, generic_views.CreateView):
    """Create a new media coverage event."""

    permission_required = 'mediacoverage.add_mediacoverage'

    def get_success_url(self):
        """
        Set up success url to redirect to after media event
        creation.

        """
        return reverse(
                'console_media_media_coverage_detail', args=(self.object.pk,)
        )


class MediaCoverageUpdate(AdminMixin, generic_views.UpdateView):
    """
    Allow users able to access the console to update
    media coverage.

    """
    permission_required = 'mediacoverage.change_mediacoverage'

    def get_success_url(self):
        """Set success url."""

        return reverse(
                'console_media_media_coverage_detail', args=(self.object.pk,)
        )

    def get_queryset(self):
        """Return a list of media coverage objects."""

        return media_models.MediaCoverage.objects.permitted().all()


class MediaCoverageDetail(AdminMixin, generic_views.DetailView):
    """Allow console users to view the details of media coverage."""

    permission_required = 'mediacoverage.change_mediacoverage'

    def get_object(self):
        """Return request media coverage object."""

        return core_utils.get_permitted_object_or_404(
            media_models.MediaCoverage, pk=self.kwargs['pk']
        )


class MediaCoverageDelete(AdminMixin, core_views.MarkDeleteView):
    """Allow users with console access to delete media coverage obj."""

    permission_required = 'mediacoverage.delete_mediacoverage'

    def get_success_url(self):
        """Set success url."""

        return reverse('console_media_media_coverage_list')

    def get_queryset(self):
        """Return all media coverage objects."""

        return media_models.MediaCoverage.objects.permitted().all()


class MediaCoverageList(AdminMixin, generic_views.ListView):
    """
    Allow users with console access to view a list
    of media coverage objects.

    """
    permission_required = 'mediacoverage.change_mediacoverage'

    def get_queryset(self):
        """Return a list of all media coverage objects."""

        return media_models.MediaCoverage.objects.permitted().all()

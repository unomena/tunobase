'''
Created on 05 Mar 2013

@author: michael
'''
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
    raise_exception = False


class MediaCoverageCreate(AdminMixin, generic_views.CreateView):
    permission_required = 'mediacoverage.add_mediacoverage'

    def get_success_url(self):
        return reverse(
                'console_media_media_coverage_detail', args=(self.object.pk,)
        )


class MediaCoverageUpdate(AdminMixin, generic_views.UpdateView):
    permission_required = 'mediacoverage.change_mediacoverage'

    def get_success_url(self):
        return reverse(
                'console_media_media_coverage_detail', args=(self.object.pk,)
        )

    def get_queryset(self):
        return media_models.MediaCoverage.objects.permitted().all()


class MediaCoverageDetail(AdminMixin, generic_views.DetailView):
    permission_required = 'mediacoverage.change_mediacoverage'

    def get_object(self):
        return core_utils.get_permitted_object_or_404(
            media_models.MediaCoverage, pk=self.kwargs['pk']
        )


class MediaCoverageDelete(AdminMixin, core_views.MarkDeleteView):
    permission_required = 'mediacoverage.delete_mediacoverage'

    def get_success_url(self):
        return reverse('console_media_media_coverage_list')

    def get_queryset(self):
        return media_models.MediaCoverage.objects.permitted().all()


class MediaCoverageList(AdminMixin, generic_views.ListView):
    permission_required = 'mediacoverage.change_mediacoverage'

    def get_queryset(self):
        return media_models.MediaCoverage.objects.permitted().all()

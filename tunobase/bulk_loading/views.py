"""
Bulk Loading App

This module provides upload and download functionality of files.

"""
import datetime
import mimetypes

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDict
from django.utils.translation import ugettext_lazy as _
from django.views import generic as generic_views

from tunobase.bulk_loading import forms, tasks
from tunobase.console import mixins as console_mixins
from tunobase.core import utils as core_utils


class BulkUploadTemplate(console_mixins.ConsoleUserRequiredMixin,
        generic_views.View):
    """Template for allowing file uploads."""

    filepath = None
    filename = None
    mimetype = None

    def get(self, request):
        """Set file name and mimetype."""

        if self.filepath is None:
            raise ImproperlyConfigured(
                _("Attribute 'filepath' is not set")
            )

        if self.filename is None:
            raise ImproperlyConfigured(
                _("Attribute 'filename' is not set")
            )

        mimetype = self.mimetype or mimetypes.guess_type(self.filename)[0]
        response = HttpResponse(mimetype=mimetype)
        response['Content-Disposition'] = \
                'attachment;filename=%s' % self.filename
        response.write(open(self.filepath, 'rb').read())
        return response


class BulkUpload(console_mixins.ConsoleUserRequiredMixin,
        generic_views.FormView):
    """Allow for multiple file uploads. """

    template_name = 'bulk_loading/bulk_upload.html'
    form_class = forms.BulkUploadForm
    validator_form_class = None
    unique_field_names = []
    bulk_updater_class = None

    def get_form_kwargs(self):
        """Get field names."""

        kwargs = super(BulkUpload, self).get_form_kwargs()

        kwargs.update({
            'validator_form': self.validator_form_class,
            'unique_field_names': self.unique_field_names
        })

        return kwargs

    def form_valid(self, form):
        """Validate form."""

        if self.bulk_updater_class is None:
            raise ImproperlyConfigured(
                _("Attribute 'bulk_updater_class' is not set")
            )

        if settings.CELERY_ALWAYS_EAGER:
            upload_data = form.save_upload_data()
            tasks.upload_data.delay(
                upload_data.pk,
                self.bulk_updater_class,
                form.cleaned_data['create'],
                form.cleaned_data['update']
            )

            messages.success(
                self.request,
                _("Your import will begin momentarily and you will be "
                "notified via email once it is complete.")
            )
        else:
            form.save(self.bulk_updater_class)

            messages.success(
                self.request,
                _("Thank you! Your import completed successfully.")
            )

        return self.render_to_response(self.get_context_data(form=form))


class BulkDownload(console_mixins.ConsoleUserRequiredMixin,
                   generic_views.ListView):
    """Allow files to be downloaded."""

    filename = None

    def render_to_response(self, context, **kwargs):
        """Render filename and file type to the browser."""

        if self.filename is None:
            raise ImproperlyConfigured(
                _("Attribute 'filename' is not set")
            )

        self.filename = self.filename % {'date': datetime.date.today()}

        response = super(BulkDownload, self).render_to_response(
            context,
            content_type='text/csv',
            **kwargs
        )
        response['Content-Disposition'] = \
                'attachment; filename="%s.csv"' % self.filename
        return response


class BulkImageUpload(generic_views.View):
    """Alow for image uploads."""

    form_class = None

    def post(self, request, *args, **kwargs):
        """Submit file upload form here."""

        data = {
            'files': MultiValueDict({
                'images': request.FILES.getlist('images[]')
            })
        }

        form = self.form_class(**data)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """Validate and save form."""
        image_ids = form.save()

        return core_utils.respond_with_json({
            'success': True,
            'image_ids': image_ids
        })

    def form_invalid(self, form):
        """Return to browser if unsuccessful."""

        return core_utils.respond_with_json({
            'success': False
        })

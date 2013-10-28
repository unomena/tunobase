'''
Created on 28 Oct 2013

@author: michael
'''
import mimetypes

from django.views import generic as generic_views
from django.core.exceptions import ImproperlyConfigured
from django import HttpResponse

from tunobase.console import mixins as console_mixins

class BulkUploadTemplate(console_mixins.ConsoleUserRequiredMixin, generic_views.View):
    filepath = None
    filename = None
    mimetype = None

    def get(self, request):
        if self.filepath is None or self.filename is None:
            raise ImproperlyConfigured(
                "Attributes `filepath` and `filename` are not set"
            )
        
        mimetype = self.mimetype or mimetypes.guess_type(self.filename)[0]
        response = HttpResponse(mimetype=mimetype)
        response['Content-Disposition'] = 'attachment;filename=%s' % self.filename
        response.write(open(self.filepath, 'rb').read())
        return response

class BulkUpload(console_mixins.ConsoleUserRequiredMixin, generic_views.FormView):
    template_name = 'bulk_loading/bulk_upload.html'
    
    def form_valid(self, form):
        return NotImplemented
    
class BulkDownload(console_mixins.ConsoleUserRequiredMixin, generic_views.ListView):
    filename = None
    
    def render_to_response(self, context, **kwargs):
        if self.filepath is None or self.filename is None:
            raise ImproperlyConfigured(
                "Attribute `filename` is not set"
            )
        
        response = super(BulkDownload, self).render_to_response(
            context,
            content_type='text/csv',
            **kwargs
        )
        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % self.filename
        return response
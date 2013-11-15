'''
Created on 28 Oct 2013

@author: michael
'''
import mimetypes
import datetime

from django.views import generic as generic_views
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDict

from tunobase.core import utils as core_utils
from tunobase.console import mixins as console_mixins
from tunobase.bulk_loading import forms

class BulkUploadTemplate(console_mixins.ConsoleUserRequiredMixin, generic_views.View):
    filepath = None
    filename = None
    mimetype = None

    def get(self, request):
        if self.filepath is None:
            raise ImproperlyConfigured(
                "Attribute 'filepath' is not set"
            )
            
        if self.filename is None:
            raise ImproperlyConfigured(
                "Attribute 'filename' is not set"
            )
        
        mimetype = self.mimetype or mimetypes.guess_type(self.filename)[0]
        response = HttpResponse(mimetype=mimetype)
        response['Content-Disposition'] = 'attachment;filename=%s' % self.filename
        response.write(open(self.filepath, 'rb').read())
        return response

class BulkUpload(console_mixins.ConsoleUserRequiredMixin, generic_views.FormView):
    template_name = 'bulk_loading/bulk_upload.html'
    form_class = forms.BulkUploadForm
    model = None
    data_key = None
    validator_form_class = None
    unique_field_names = []
    
    def get_form_kwargs(self):
        kwargs = super(BulkUpload, self).get_form_kwargs()
        
        kwargs.update({
            'validator_form': self.validator_form_class,
            'unique_field_names': self.unique_field_names
        })

        return kwargs
    
    def get_object(self, data):
        if self.data_key is None:
            raise ImproperlyConfigured(
                "Attribute 'data_key' is not set"
            )
            
        if self.model is None:
            raise ImproperlyConfigured(
                "Attribute 'model' is not set"
            )
        
        try:
            kwargs = {
                self.data_key: data[self.data_key]
            }
            return self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            return None
    
    def bulk_create_objects(self, object_list):
        return NotImplemented
    
    def create_object(self, data):
        return NotImplemented
    
    def update_object(self, obj, data, created):
        return NotImplemented
    
    def form_valid(self, form):
        use_celery = getattr(settings, 'USE_CELERY_FOR_BULK_UPLOADING', False)
        if use_celery:
            upload_data = form.save_upload_data()
            tasks.upload_data.delay(upload_data.id)
        else:
            form.save(
                self.get_object, 
                self.create_object, 
                self.update_object,
                self.bulk_create_objects
            )
            
            messages.success(
                self.request,
                "Thank you! Your import completed successfully."
            )
        
        return self.render_to_response(self.get_context_data(form=form))
    
class BulkDownload(console_mixins.ConsoleUserRequiredMixin, generic_views.ListView):
    filename = None
    
    def render_to_response(self, context, **kwargs):
        if self.filename is None:
            raise ImproperlyConfigured(
                "Attribute 'filename' is not set"
            )
            
        self.filename = self.filename % {'date': datetime.date.today()}
        
        response = super(BulkDownload, self).render_to_response(
            context,
            content_type='text/csv',
            **kwargs
        )
        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % self.filename
        return response
    
class BulkImageUpload(generic_views.View):
    form_class = None
    
    def post(self, request, *args, **kwargs):
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
        image_ids = form.save()
        
        return core_utils.respond_with_json({
            'success': True,
            'image_ids': image_ids
        })
        
    def form_invalid(self, form):
        print form.errors
        
        return core_utils.respond_with_json({
            'success': False
        })
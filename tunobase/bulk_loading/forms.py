'''
Created on 28 Oct 2013

@author: michael
'''
import hashlib
import csv

from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.contrib import messages

from tunobase.bulk_loading import models

class BulkUploadForm(forms.Form):
    '''
    Form accepting and validating CSV file, returning collection of validated
    dictionaries to import.
    '''
    duplicate_file_reimport = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput()
    )
    create = forms.BooleanField(required=False)
    update = forms.BooleanField(required=False)
    upload_file = forms.FileField()
    
    def __init__(self, *args, **kwargs):
        self.validator_form = kwargs.pop('validator_form', None)
        self.unique_field_names = kwargs.pop('unique_field_names', [])
        
        if self.validator_form is None:
            raise ImproperlyConfigured(
                "kwargs `validator_form` is required"
            )
        super(BulkUploadForm, self).__init__(*args, **kwargs)
        
    def _check_file_previously_uploaded(self):
        '''
        Check if the file has been previously uploaded
        '''
        self.uploaded_file = self.cleaned_data['upload_file']
        self.md5 = hashlib.md5(self.uploaded_file.read()).hexdigest()
        if not self.cleaned_data['duplicate_file_reimport']:
            try:
                models.BulkUploadHash.objects.get(md5=self.md5)
                self.data['duplicate_file_reimport'] = u'on'
                raise forms.ValidationError(
                    "%s appears to have been imported previously. If you "
                    "want to re-import it please specify it again and "
                    "click import. Note: this might cause data "
                    "duplication." % self.uploaded_file.name
                )
            except models.BulkUploadHash.DoesNotExist:
                pass
            
    def _process_uploaded_file(self):
        '''
        Process the uploaded file
        '''
        self.uploaded_file.seek(0)
        reader = csv.reader(self.uploaded_file, delimiter=',')
        valid_rows = []
        unique_fields = []
        for i, row in enumerate(reader):
            if i == 0:
                keys = row
            else:
                data = {}
                for j, value in enumerate(row):
                    data[keys[j]] = value
                csv_form = self.validator_form(data, update=self.cleaned_data['update'])
                
                if csv_form.is_valid():
                    data = csv_form.cleaned_data
                    unique_field_data = ''.join([
                        data[unique_field_name] for unique_field_name in self.unique_field_names
                    ])
                    
                    if unique_field_data and unique_field_data in unique_fields:
                        raise forms.ValidationError(
                            'Data "%s" appears multiple times in your '
                            'CSV data. Please ensure data is unique.'
                            % ', '.join([
                                data[unique_field_name] for unique_field_name in self.unique_field_names
                            ])
                        )
                    else:
                        unique_fields.append(unique_field_data)
                        valid_rows.append(data)
                else:
                    csv_errors = []
                    for key, value in csv_form.errors.items():
                        csv_errors.append(
                            '%s value of "%s" is invalid (row %s). %s'
                            % (key, data[key], i, value[0])
                        )
                    raise forms.ValidationError(csv_errors)
                
        models.BulkUploadHash.objects.get_or_create(md5=self.md5)
        return valid_rows

    def clean_upload_file(self):
        self._check_file_previously_uploaded()
        
        return self._process_uploaded_file()

    @transaction.atomic
    def save(self, request, get_obj_callback, create_obj_callback, 
             update_obj_callback, bulk_create_callback, *args, **kwargs):
        '''
        Save uploaded objects
        '''
        create = self.cleaned_data['create']
        update = self.cleaned_data['update']
        
        # If we're only creating objects, then bulk
        # insert them to optimize performance
        if create and not update:
            objs = []
            for data in self.cleaned_data['upload_file']:
                obj = create_obj_callback(data)
                objs.append(obj)
            bulk_create_callback(objs)
        else:
            for data in self.cleaned_data['upload_file']:
                created = False
                
                obj = get_obj_callback(data)
    
                if obj is None and create:
                    obj = create_obj_callback(data)
                    created = True
    
                if created or update:
                    # Set simple fields.
                    update_obj_callback(obj, data, created)

        messages.success(
            request,
            "Thank you! Your import completed successfully."
        )
        
class BulkUploadValidatorForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.update = kwargs.pop('update', False)
        super(BulkUploadValidatorForm, self).__init__(*args, **kwargs)
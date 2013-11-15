'''
Created on 28 Oct 2013

@author: michael
'''
from celery.decorators import task

from django.utils import timezone

@task(ignore_result=True)
def clear_unused_bulk_uploaded_images():
    '''
    Remove all bulk uploaded images longer than a day old
    '''
    from tunobase.bulk_loading import models
    
    time_to_live = timezone.now() - timezone.timedelta(days=1)
    models.BulkUploadImage.objects.filter(created_at__lt=time_to_live).delete()
    
@task(default_retry_delay=10 * 60)
def upload_data(upload_data_id):
    '''
    Bulk upload data in a celery task
    '''
    try:
        from tunobase.bulk_loading import models
        
        bulk_upload_data = models.BulkUploadData.objects.get(pk=upload_data_id)
        
        #todo: finish this
    except Exception, exc:
        raise upload_data.retry(exc=exc)
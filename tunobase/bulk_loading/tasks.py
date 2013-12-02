'''
Created on 28 Oct 2013

@author: michael
'''
from celery.decorators import task

from django.utils import timezone
from django.core.mail import mail_admins
from django.conf import settings

@task(ignore_result=True)
def clear_unused_bulk_uploaded_images():
    '''
    Remove all bulk uploaded images longer than a day old
    '''
    from tunobase.bulk_loading import models
    
    time_to_live = timezone.now() - timezone.timedelta(days=1)
    models.BulkUploadImage.objects.filter(created_at__lt=time_to_live).delete()
    
@task(default_retry_delay=10 * 60)
def upload_data(upload_data_pk, bulk_updater_class, create, update):
    '''
    Bulk upload data in a celery task
    '''
    try:
        from tunobase.bulk_loading import models
        
        bulk_upload_data, obj = models.BulkUploadData.objects.get_decoded_data(upload_data_pk)
        
        if bulk_upload_data is not None:
            bulk_updater = bulk_updater_class(bulk_upload_data)
            bulk_updater.save(create, update)
            obj.delete()
            
            mail_admins(
                '%s Celery Bulk Import Complete' % settings.APP_NAME, 
                'Your celery bulk import on %s has completed.' % settings.APP_NAME
            )
    except Exception, exc:
        raise upload_data.retry(exc=exc)
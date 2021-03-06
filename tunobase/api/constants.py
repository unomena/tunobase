"""
API App

This module lists the default settings for the API app.

"""
REQUEST_STATUS_CREATED = 0
REQUEST_STATUS_SUCCESS = 1
REQUEST_STATUS_ERROR = 2
REQUEST_STATUS_RETRY = 3
REQUEST_STATUS_ABORT = 4

REQUEST_STATUS_CHOICES = (
    (REQUEST_STATUS_CREATED, 'Created'),
    (REQUEST_STATUS_SUCCESS, 'Success'),
    (REQUEST_STATUS_ERROR, 'Error'),
    (REQUEST_STATUS_RETRY, 'Retry'),
    (REQUEST_STATUS_ABORT, 'Abort'),
)

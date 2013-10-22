'''
Created on 22 Oct 2013

@author: michael
'''
STATE_PUBLISHED = 0
STATE_UNPUBLISHED = 1
STATE_STAGED = 2
STATE_DELETED = 3

STATE_CHOICES = (
    (STATE_PUBLISHED, 'Published'),
    (STATE_UNPUBLISHED, 'Unpublished'),
    (STATE_STAGED, 'Staged'),
    (STATE_DELETED, 'Deleted'),
)
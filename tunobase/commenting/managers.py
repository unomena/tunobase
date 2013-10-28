'''
Created on 28 Oct 2013

@author: michael
'''
from django.contrib.comments import managers as comment_managers

from tunobase.core import managers as core_managers

class CommentManager(core_managers.StateManagerMixin, comment_managers.CommentManager):
    pass
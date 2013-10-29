'''
Created on 28 Oct 2013

@author: michael
'''
from django.db import models
from django.contrib.comments import models as comment_models, managers as comment_managers
from django.contrib.auth.models import Permission
from django.contrib.sites.models import Site
from django.conf import settings

from tunobase.core import models as core_models
from tunobase.commenting import managers, constants

class CommentModel(core_models.StateModel, core_models.AuditModel, 
                   comment_models.BaseCommentAbstractModel):
    '''
    Comments to be used throughout the Site
    '''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        blank=True, 
        null=True, 
        related_name="comments"
    )
    user_name = models.CharField(max_length=255, blank=True, null=True)
    user_email = models.EmailField(blank=True, null=True)
    user_url = models.URLField(blank=True, null=True)

    comment = models.TextField(max_length=3000)

    # Metadata about the comment
    ip_address = models.IPAddressField(blank=True, null=True)
    is_removed = models.BooleanField(default=False)
    
    in_reply_to = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        related_name='replies'
    )
    moderated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='comments_moderated', 
        null=True, 
        blank=True
    )
    moderated_at = models.DateTimeField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    
    objects = comment_managers.CommentManager()
    permitted = managers.CommentManager()

    class Meta:
        permissions = [
            ("can_moderate", "Can moderate comments"),
            ("view_comment", "View comment")
        ]
        ordering = ('-order', '-publish_at',)
        
    def __unicode__(self):
        return u'%s' % self.comment
    
    @property
    def author(self):
        if self.user is None:
            return self.user_name
        
        return self.user.display_name
        
class CommentFlag(core_models.AuditModel):
    '''
    Records a flag on a comment.
    '''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        blank=True, 
        null=True, 
        related_name="commentmodel_flags"
    )
    comment = models.ForeignKey(CommentModel, related_name="flags")
    flag = models.CharField(
        choices=constants.FLAG_CHOICES, 
        max_length=30, 
        db_index=True
    )

    class Meta:
        unique_together = [('user', 'comment', 'flag')]

    def __unicode__(self):
        return u"%s flag of comment ID %s by %s" % \
            (self.flag, self.comment_id, self.user.get_username())
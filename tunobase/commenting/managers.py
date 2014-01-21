"""
Commenting App

This module provides an interface into retrieving comments
and removing them where necessary.

"""
from django.conf import settings
from django.contrib.comments import managers as comment_managers
from django.db import models

from tunobase.commenting import query, constants
from tunobase.core import managers as core_managers


class CommentManager(core_managers.CoreStateManager,
                     comment_managers.CommentManager):
    """
    Comment Manager for retrieving the amount of comments
    for a given Content Object and removing flagged comments
    passing the threshold

    """

    def get_queryset(self):
        """Return relevant comment object."""

        return query.CommentQuerySet(self.model, using=self._db)

    def get_comments_for_object(self, content_type_id, object_pk, site=None):
        """Return all the comments for a particular object."""

        return self.get_queryset().get_comments_for_object(
            content_type_id,
            object_pk,
            site
        )

    def remove_flagged_comments(self):
        """
        Work out if a comment should be removed based
        on the number of removal requests it receives.
        If more than 5, mark is as removed.

        """
        for comment in self.permitted():
            num_removal_flags = comment.flags.filter(
                flag=constants.FLAG_SUGGEST_REMOVAL
            ).count()
            if num_removal_flags >= getattr(settings,
               'COMMENT_FLAGS_FOR_REMOVAL', 5):
                comment.is_removed = True
                comment.save()


class CommentFlagManager(models.Manager):
    """Comment flag manager used for flagging comments."""

    def report(self, user, comment_id):
        """Create a flagged for removal object."""

        self.create(
            user=user,
            comment_id=comment_id,
            flag=constants.FLAG_SUGGEST_REMOVAL
        )

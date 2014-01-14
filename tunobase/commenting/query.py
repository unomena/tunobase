"""
Commenting App

This module retrieves all the comments for an object.

Classes:
    CommentQuerySet

Functions:
    n/a

Created on 25 Oct 2013

@author: michael

"""
from django.contrib.sites.models import Site

from tunobase.core import query as core_query


class CommentQuerySet(core_query.CoreStateQuerySet):
    """Get all comments for particular object."""

    def get_comments_for_object(self, content_type_id, object_pk, site=None):
        """Get all the comments for an object.

        Keyword arguments:
        site -- set site to current site (default is None)

        """
        if site is None:
            site = Site.objects.get_current()

        return self.select_related('user').filter(
            content_type_id=content_type_id,
            object_pk=object_pk,
            site=site
        )

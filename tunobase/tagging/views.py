"""
TAGGING APP

This module provides an interface for users to interact with
the taggin app.

Classes:
    RetrieveTags
    UpdateTags

Functions:
    n/a

Created on 29 Oct 2013

@author: michael

"""
from django.views import generic as generic_views

from tunobase.core import utils as core_utils
from tunobase.tagging import models

class RetrieveTags(generic_views.View):
    """Retrieve all the tags for an object."""

    def get(self, request, *args, **kwargs):
        """Get tags."""

        term = request.GET.get('term', '')

        return core_utils.respond_with_json(
            [tag.title for tag in models.Tag.objects\
                    .for_current_site()\
                    .filter(title__icontains=term)
            ]
        )


class UpdateTags(generic_views.FormView):
    """Update tags for an object."""

    def form_valid(self, form):
        """Save new tags."""

        form.save(self.request.POST.getlist('tags', []))

        return core_utils.respond_with_json({
            'success': True
        })

    def form_invalid(self, form):
        """Fail form validation and render form again."""

        return core_utils.respond_with_json({
            'success': False
        })

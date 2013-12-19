"""
TAGGING APP

This module is used to describe the forms used for the tagging app.

Classes:
    TagUpdateForm

Functions:
    n/a

Created on 29 Oct 2013

@author: michael

"""
from django import forms
from django.contrib.sites.models import Site

from tunobase.tagging import models

class TagUpdateForm(forms.Form):
    """Save new tags in the database."""

    tag_content_type_id = forms.IntegerField()
    tag_object_pk = forms.CharField()

    def save(self, tags):
        """
        For each tag received in the POST method,
        ensure the tag doesn't already exist and save.

        """
        tags = set(tags)
        site = Site.objects.get_current()
        content_object_tags = []

        # delete all existing tags on the object
        models.ContentObjectTag.objects.filter(
            site=site,
            content_type_id=self.cleaned_data['tag_content_type_id'],
            object_pk=self.cleaned_data['tag_object_pk']
        ).delete()

        # iterate tags received in POST data and create new tags
        # for them if applicable
        for tag in tags:
            tag_model, _ = models.Tag.objects.get_or_create(
                site=site,
                title=tag
            )

            content_object_tag = models.ContentObjectTag(
                site=site,
                content_type_id=self.cleaned_data['tag_content_type_id'],
                object_pk=self.cleaned_data['tag_object_pk'],
                tag=tag_model
            )

            content_object_tags.append(content_object_tag)

        # add the new tags to the object if any were created
        if content_object_tags:
            models.ContentObjectTag.objects.bulk_create(content_object_tags)

        return content_object_tags

'''
Created on 02 Dec 2013

@author: euan
'''
from django.template.defaultfilters import slugify
from django.test import TestCase
from django.utils import timezone

from tunobase.core import constants, models

class ContentModelTestCase(TestCase):
    title = 'Content Model Test Case Title'
    slug = slugify(title)

    def setUp(self):
        '''
        Create the Content Model in the Database
        '''
        models.ContentModel.objects.create(title=self.title)

    def test_state_model(self):
        '''
        Test that the state is correct
        '''
        published_object = models.ContentModel.objects.get(slug=self.slug)
        self.assertEqual(published_object.state, constants.STATE_PUBLISHED)

        published_object.state = constants.STATE_UNPUBLISHED
        published_object.save()
        try:
            published_object = models.ContentModel.objects\
                    .permitted()\
                    .get(slug=self.slug)
        except models.ContentModel.DoesNotExist:
            published_object = None

        self.assertIsNone(published_object, 'Permitted Manager failed')

        published_object = models.ContentModel.objects.get(slug=self.slug)
        published_object.mark_deleted()

        deleted_object = models.ContentModel.objects.get(slug=self.slug)
        self.assertEqual(deleted_object.state, constants.STATE_DELETED)

    def test_slug_model(self):
        '''
        Test that the slug gets created.
        '''
        title_object = models.ContentModel.objects.get(title=self.title)
        self.assertEqual(title_object.title, self.title)
        self.assertEqual(title_object.slug, self.slug)

        slug_object = models.ContentModel.objects.get(slug=self.slug)
        self.assertEqual(slug_object.title, self.title)
        self.assertEqual(slug_object.slug, slugify(self.title))

    def test_audit_model(self):
        audit_object = models.ContentModel.objects.get(slug=self.slug)

        self.assertLessEqual(audit_object.created_at, timezone.now())
        self.assertLessEqual(audit_object.modified_at, timezone.now())

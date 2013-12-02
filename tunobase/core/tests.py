'''
Created on 02 Dec 2013

@author: euan
'''
from django.test import TestCase
from django.template.defaultfilters import slugify

from tunobase.core import constants, models

class ContentModelTestCase(TestCase):

    title = 'Content Model Test Case Title'
    slug = 'content-model-test-case-title'

    def setUp(self):
        models.ContentModel.objects.create(title=self.title)


    def tearDown(self):
        pass


    def test_state_model(self):
        published_object = models.ContentModel.objects.get(slug=self.slug)
        self.assertEqual(published_object.state, constants.STATE_PUBLISHED)
        
        published_object.state = constants.STATE_UNPUBLISHED
        published_object.save()
        try:
            published_object = models.ContentModel.objects.permitted.get(slug=self.slug)
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
        pass
    
    def test_image_model(self):
        pass
    
    def test_base_content_model(self):
        pass
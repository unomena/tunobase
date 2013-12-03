'''
Created on 03 Dec 2013

@author: michael
'''
from django.test import TestCase
from django.utils import timezone

from tunobase.social_media.tunosocial import models

class LikeModelTestCase(TestCase):
    ip_address = '127.0.0.1'

    def setUp(self):
        '''
        Create the Like Model
        '''
        models.Like.objects.create(
            ip_address=self.ip_address,
            content_type_id=1,
            object_pk=1,
            site_id=1
        )

    def test_like_model(self):
        '''
        Test that the Like was created successfully
        '''
        like_object = models.Like.objects.get(pk=1)
        self.assertEqual(like_object.ip_address, self.ip_address)
        self.assertEqual(like_object.content_type_id, 1)
        self.assertEqual(like_object.object_pk, 1)
        self.assertEqual(like_object.site_id, 1)
        self.assertLessEqual(like_object.created_at, timezone.now())
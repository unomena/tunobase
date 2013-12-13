'''
Created on 02 Dec 2013

@author: euan
'''
from django.conf import settings
from django.test import TestCase

from tunobase.commenting import models, constants
from tunobase.core import constants as core_constants

class CommentModelTestCase(TestCase):
    comment = 'Comment Model Test Case Comment'
    comment_reply = 'Comment Model Test Case Comment Reply'
    comment_user_name = 'test'
    comment_user_email = 'test@example.com'
    comment_user_url = 'http://example.com'
    ip_address = '127.0.0.1'
    flag = constants.FLAG_SUGGEST_REMOVAL

    def setUp(self):
        '''
        Create the Comment Model, a Reply to the Comment Model and
        enough flags to mark the Comment Model as removed in the database
        '''
        self.comment_object = models.CommentModel.objects.create(
            comment=self.comment,
            ip_address=self.ip_address,
            user_name=self.comment_user_name,
            user_email=self.comment_user_email,
            user_url=self.comment_user_url,
            content_type_id=1,
            site_id=1
        )
        models.CommentModel.objects.create(
            comment=self.comment_reply,
            in_reply_to=self.comment_object,
            content_type_id=1,
            site_id=1
        )
        for i in range(settings.COMMENT_FLAGS_FOR_REMOVAL):
            models.CommentFlag.objects.create(
                comment=self.comment_object,
                flag=self.flag
            )

    def test_comment_model(self):
        '''
        Test that the Comment was created with the right comment, state,
        ip_address, user_name, user_email, user_url and has at least one Reply
        '''
        comment_object = models.CommentModel.objects.get(comment=self.comment)
        self.assertEqual(comment_object.comment, self.comment)
        self.assertEqual(comment_object.state, core_constants.STATE_PUBLISHED)
        self.assertEqual(comment_object.ip_address, self.ip_address)
        self.assertEqual(comment_object.user_name, self.comment_user_name)
        self.assertEqual(comment_object.user_email, self.comment_user_email)
        self.assertEqual(comment_object.user_url, self.comment_user_url)
        self.assertGreaterEqual(comment_object.replies.count(), 1)

    def test_comment_flags(self):
        '''
        Test that when a Comment is flagged a certain amount of times, 
        it gets marked as removed
        '''
        self.assertEqual(
                self.comment_object.flags.count(),
                settings.COMMENT_FLAGS_FOR_REMOVAL
        )
        models.CommentModel.objects.remove_flagged_comments()
        comment_object = models.CommentModel.objects.get(comment=self.comment)
        self.assertTrue(comment_object.is_removed)

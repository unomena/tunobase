"""
Blog App

This module provides test functionality for the blog app.

"""
from django.template.defaultfilters import slugify
from django.test import TestCase

from tunobase.blog import models
from tunobase.core import constants as core_constants


class BlogModelTestCase(TestCase):
    """
    Provide the test cases to test the blog model.

    """
    title = 'Blog Model Test Case Title'
    entry_title = 'Blog Entry Model Test Case Title'
    alternate_authors = 'Michael Whelehan,Euan Jonker'
    alternate_authors_splitted = ['Michael Whelehan', 'Euan Jonker']
    slug = slugify(title)
    entry_slug = slugify(entry_title)

    def setUp(self):
        """Create the Blog and Blog Entry Models in the database."""

        self.blog = models.Blog.objects.create(title=self.title)
        models.BlogEntry.objects.create(
            title=self.entry_title,
            blog=self.blog,
            authors_alternate=self.alternate_authors
        )

    def test_blog_model(self):
        """
        Test that the Blog was created with the right slug, state
        and has at least one Blog Entry

        """
        blog_object = models.Blog.objects.get(slug=self.slug)
        self.assertEqual(blog_object.slug, self.slug)
        self.assertEqual(blog_object.state, core_constants.STATE_PUBLISHED)
        self.assertGreaterEqual(blog_object.entries.count(), 1)

    def test_blog_entry_model(self):
        """
        Test that the Blog Entry was created with the right slug, state
        and that the alternate authors are returned correctly

        """
        blog_entry_object = models.BlogEntry.objects.get(blog=self.blog)
        self.assertEqual(blog_entry_object.slug, self.entry_slug)
        self.assertEqual(
                blog_entry_object.state,
                core_constants.STATE_PUBLISHED
        )
        self.assertEqual(
                blog_entry_object.authors_alternate,
                self.alternate_authors
        )
        self.assertEqual(
                blog_entry_object.authors['alternate'],
                self.alternate_authors_splitted
        )

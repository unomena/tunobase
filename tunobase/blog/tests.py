'''
Created on 02 Dec 2013

@author: euan
'''
from django.test import TestCase
from django.template.defaultfilters import slugify

from tunobase.core import constants as core_constants
from tunobase.blog import models

class BlogModelTestCase(TestCase):
    title = 'Blog Model Test Case Title'
    entry_title = 'Blog Entry Model Test Case Title'
    alternate_authors = 'Michael Whelehan,Euan Jonker'
    alternate_authors_splitted = ['Michael Whelehan', 'Euan Jonker']
    slug = slugify(title)
    entry_slug = slugify(entry_title)

    def setUp(self):
        self.blog = models.Blog.objects.create(title=self.title)
        models.BlogEntry.objects.create(
            title=self.entry_title,
            blog=self.blog, 
            authors_alternate=self.alternate_authors
        )

    def test_blog_model(self):
        blog_object = models.Blog.objects.get(slug=self.slug)
        self.assertEqual(blog_object.slug, self.slug)
        self.assertEqual(blog_object.state, core_constants.STATE_PUBLISHED)
        self.assertGreaterEqual(blog_object.entries.all(), 1)
    
    def test_blog_entry_model(self):
        blog_entry_object = models.BlogEntry.objects.get(blog=self.blog)
        self.assertEqual(blog_entry_object.slug, self.entry_slug)
        self.assertEqual(blog_entry_object.state, core_constants.STATE_PUBLISHED)
        self.assertEqual(blog_entry_object.authors_alternate, self.alternate_authors)
        self.assertEqual(blog_entry_object.authors['alternate'], self.alternate_authors_splitted)
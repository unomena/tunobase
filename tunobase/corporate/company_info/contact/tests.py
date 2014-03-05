'''
Created on 24 Feb 2014

@author: michael
'''
from django.test import TestCase, Client
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

from tunobase.corporate.company_info.contact import models as contact_models


class ContactTestCase(TestCase):
    """Set up the Contact model test cases."""

    def setUp(self):
        """Create Client and Contact Models"""
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='test'
        )
        self.contact_object = contact_models.ContactMessage.objects.create(
            user=self.user,
            name='Joe Soap',
            email='joe@soap.com',
            mobile_number='071 123 4567',
            message='Test message',
        )
        self.contact_object_non_required = contact_models.ContactMessage\
            .objects.create(
                name='Joe Blogs',
                email='joe@blogs.com',
                message='Test message',
            )

    def test_contact_model(self):
        """
        Test that the Contact Models were created with the
        correct values

        """
        contact_object = contact_models.ContactMessage.objects.get(
            user=self.user
        )
        self.assertEqual(contact_object, self.contact_object)

        contact_object_non_required = contact_models.ContactMessage\
            .objects.get(
                name='Joe Blogs'
            )
        self.assertEqual(
            contact_object_non_required,
            self.contact_object_non_required
        )

    def test_contact_view(self):
        """
        Test that the Contact FormView works as expected

        """
        response = self.client.post(
            '/about-us/contact/',
            {
                'name': 'Joe Soap',
                'email': 'joe@soap.com',
                'mobile_number': '071 123 4567',
                'message': 'Test message',
                'tim_hp': 'tim'
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_contact_view_authenticated(self):
        """
        Test that the Contact FormView works as expected for an
        authenticated user

        """
        self.client.login(username='test@example.com', password='test')
        response = self.client.post(
            '/about-us/contact/',
            {
                'name': 'Joe Soap',
                'email': 'joe@soap.com',
                'mobile_number': '071 123 4567',
                'message': 'Test message',
                'tim_hp': 'tim'
            }
        )
        self.assertEqual(response.status_code, 302)

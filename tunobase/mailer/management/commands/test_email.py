'''
Created on 10 Apr 2014

@author: euan
'''
from django.core.management.base import BaseCommand
from django.conf import settings

from tunobase.mailer import utils as mailer_utils


class Command(BaseCommand):
    """
    Test the email setup.
    """
    def handle(self, *args, **options):
        email_address = args[0]
        print 'Sending test email to: %s' % email_address
        mailer_utils.send_mail(
            'Test message',
            'Test message',
            [email_address],
            settings.DEFAULT_FROM_EMAIL,
            html_content='Test Message'
        )

'''
Created on 04 Nov 2013

@author: michael
'''
from django.utils.http import int_to_base36

from tunobase.corporate.company_info.newsletter.tokens \
        import NewsletterUnsubscribeTokenGenerator

token_generator = NewsletterUnsubscribeTokenGenerator()

def get_uid_and_token(newsletter_recipient):
    return int_to_base36(newsletter_recipient.pk), \
        token_generator.make_token(newsletter_recipient)

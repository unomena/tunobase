'''
Created on 04 Nov 2013

@author: michael
'''
from datetime import date

from django.utils.http import int_to_base36, base36_to_int
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils import six

class NewsletterUnsubscribeTokenGenerator(object):
    '''
    Strategy object used to generate and check tokens for the
    newsletter unsubscribe mechanism.
    '''
    def make_token(self, newsletter_recipient):
        """
        Returns a token that can be used once to do a newsletter unsubscribe
        for the given user.
        """
        return self._make_token_with_timestamp(
                newsletter_recipient, self._num_days(self._today())
        )

    def check_token(self, newsletter_recipient, token):
        '''
        Check that a newsletter unsubscribe token is correct
        for a given recipient.
        '''
        # Parse the token
        try:
            ts_b36, hash = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(
                self._make_token_with_timestamp(
                    newsletter_recipient, ts
                ), token
        ):
            return False

        return True

    def _make_token_with_timestamp(self, newsletter_recipient, timestamp):
        # timestamp is number of days since 2001-1-1.  Converted to
        # base 36, this gives us a 3 digit string until about 2121
        ts_b36 = int_to_base36(timestamp)

        # We limit the hash to 20 chars to keep URL short
        key_salt = "tunobase.corporate.company_info.\
                newsletter.NewsletterUnsubscribeTokenGenerator"

        # Ensure results are consistent across DB backends
        value = (six.text_type(newsletter_recipient.pk) + \
                six.text_type(timestamp))
        hash = salted_hmac(key_salt, value).hexdigest()[::2]
        return "%s-%s" % (ts_b36, hash)

    def _num_days(self, dt):
        return (dt - date(2001, 1, 1)).days

    def _today(self):
        # Used for mocking in tests
        return date.today()

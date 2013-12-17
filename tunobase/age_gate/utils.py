"""
This module is used within the age_gate.middleware module. It redirects
the user to the home page should they meet the age gate requirements.

Classes:
    n/a

Functions:
    redirect_to_age_gate - redirect to login page

Created on 23 Oct 2013

@author: michael

"""
try:
    from urllib.parse import urlparse, urlunparse
except ImportError:     # Python 2
    from urlparse import urlparse, urlunparse

from django.http import HttpResponseRedirect, QueryDict

def redirect_to_age_gate(next, age_gate_url=None,
                      redirect_field_name='next'):
    """
    Redirects the user to the login page, passing the given 'next' page

    Keyword arguments:
    age_gate_url -- retrieved from settings (default None)
    redirect_field_name -- URI to move on to (default 'next')

    """

    login_url_parts = list(urlparse(age_gate_url))
    if redirect_field_name:
        querystring = QueryDict(login_url_parts[4], mutable=True)
        querystring[redirect_field_name] = next
        login_url_parts[4] = querystring.urlencode(safe='/')

    return HttpResponseRedirect(urlunparse(login_url_parts))

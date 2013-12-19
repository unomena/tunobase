"""
EULA APP

This module provides a utility function to redirect the user to
the login page after accepting the EULA.

Classes:
    n/a

Functions:
    redirect_to_eula

Created on 23 Oct 2013

@author: michael

"""
try:
    from urllib.parse import urlparse, urlunparse
except ImportError:     # Python 2
    from urlparse import urlparse, urlunparse

from django.http import HttpResponseRedirect, QueryDict

def redirect_to_eula(next, eula_url=None,
                     redirect_field_name='next'):
    """
    Redirects the user to the login page, passing the given 'next' page

    """
    login_url_parts = list(urlparse(eula_url))
    if redirect_field_name:
        querystring = QueryDict(login_url_parts[4], mutable=True)
        querystring[redirect_field_name] = next
        login_url_parts[4] = querystring.urlencode(safe='/')

    return HttpResponseRedirect(urlunparse(login_url_parts))

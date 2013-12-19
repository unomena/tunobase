"""
GOOGLE PLUS APP

This module provides utility functions for the Google Plus app.

Classes:
    n/a

Functions:
    flow_from_clientsecrets

Created on 09 Nov 2013

@author: michael

"""
import sys

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse_lazy

from oauth2client import util, clientsecrets
from oauth2client.client import (
        OAuth2WebServerFlow,
        UnknownClientSecretsFlowError
)


@util.positional(2)
def flow_from_clientsecrets(scope, redirect_uri=None,
                            message=None, cache=None):
    """Create a Flow from a clientsecrets file.

    Will create the right kind of Flow based on the contents of the
    clientsecrets file or will raise InvalidClientSecretsError for unknown
    types of Flows.

    Args:
      filename: string, File name of client secrets.
      scope: string or iterable of strings, scope(s) to request.
      redirect_uri: string, Either the string 'urn:ietf:wg:oauth:2.0:oob' for
        a non-web-based application, or a URI that handles the callback from
        the authorization server.
      message: string, A friendly string to display to the user if the
        clientsecrets file is missing or invalid. If message is provided then
        sys.exit will be called in the case of an error. If message in not
        provided then clientsecrets.InvalidClientSecretsError will be raised.
      cache: An optional cache service client that implements get() and set()
        methods. See clientsecrets.loadfile() for details.

    Returns:
      A Flow object.

    Raises:
      UnknownClientSecretsFlowError if the file describes an unknown kind of
      Flow.
      clientsecrets.InvalidClientSecretsError if the clientsecrets file is
        invalid.

    """
    try:
        client_type, client_info = ("web", settings.GOOGLE_PLUS_CLIENT_INFO)
        if client_type in (clientsecrets.TYPE_WEB,
                clientsecrets.TYPE_INSTALLED):
            constructor_kwargs = {
                'redirect_uri': redirect_uri,
                'auth_uri': client_info['auth_uri'],
                'token_uri': client_info['token_uri'],
            }
            revoke_uri = client_info.get('revoke_uri')
            if revoke_uri is not None:
                constructor_kwargs['revoke_uri'] = revoke_uri
            return OAuth2WebServerFlow(
                client_info['client_id'], client_info['client_secret'],
                scope, **constructor_kwargs
            )

    except clientsecrets.InvalidClientSecretsError:
        if message:
            sys.exit(message)
        else:
            raise
    else:
        raise UnknownClientSecretsFlowError(
            'This OAuth 2.0 flow is unsupported: %r' % client_type
        )

FLOW = flow_from_clientsecrets(
    scope='https://www.googleapis.com/auth/userinfo.profile '
        'https://www.googleapis.com/auth/userinfo.email',
    redirect_uri='http://%s%s' % (
        Site.objects.get_current().domain,
        reverse_lazy('google_plus_login_callback')
    )
)

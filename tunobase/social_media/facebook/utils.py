'''
Created on 09 Nov 2013

@author: michael
'''
import urllib2
import urllib
import json

from django.conf import settings

import facebook

def validate_access_token(access_token):
    '''
    Validate a Facebook access token
    '''
    # Get an app access token
    app_token = facebook.get_app_access_token(
        settings.FACEBOOK_APP_ID, 
        settings.FACEBOOK_APP_SECRET
    )
    args = {
        'input_token': access_token,
        'access_token': app_token
    }

    file = urllib2.urlopen(
        "https://graph.facebook.com/debug_token?" + urllib.urlencode(args)
    )

    try:
        result = json.loads(file.read())
    finally:
        file.close()

    return result['data']['is_valid'], result['data']['user_id']
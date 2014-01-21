'''
VUMI API

Connects to VUMI with an API account key & access token.
Sends SMS.

'''
import json

from django.conf import settings

import requests


def send_sms(msg, recipients, msg_id=None, reply_url=None):
    for recipient in recipients:
        response = requests.put(
            settings.VUMI_URL,
            auth=(settings.VUMI_ACCOUNT_KEY, settings.VUMI_ACCESS_TOKEN),
            data=json.dumps({
                'content': msg,
                'to_addr': recipient,
            }),
            verify=False
        )

    return response.json()

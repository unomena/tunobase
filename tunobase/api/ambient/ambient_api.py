'''
Created on 02 Dec 2011

@author: euan
'''
import urllib2
import xml.etree.ElementTree as ET

from django.conf import settings

# Access Settings
API_KEY = settings.AMBIENT_API_KEY
API_PASSWORD = settings.AMBIENT_API_PASSWORD

# Optional Settings
# optionally set to 0 to return an error if duplicate mobile numbers are sent
ALLOW_DUPLICATES = 1
# optionally set to 1 to allow API to carry on sending the message if and
# invalid number is found
ALLOW_INVALID_NUMBERS = 0

# Ambient Mobile SMS API
VERSION = 1.3
SMS_API_URL = getattr(
        settings, 'AMBIENT_URL', 'http://services.ambientmobile.co.za/sms/'
)
USER_AGENT = 'AM Python SMS API v' + unicode(VERSION)

MSG_CODES = {
  # Success
  '0': 'Message successfully submitted',
  '1': 'Message successfully submitted, but contained recipient errors',
  '2': 'Message successfully submitted, but contained duplicates and '
       'recipient errors',
  '1000': 'Message successfully submitted, but contained duplicates',
  # Failure
  '1001': 'Invalid HTTP POST',
  '1002': 'HTTP Post Empty no XML string found',
  '1003': 'Malformed XML',
  '1004': 'Invalid XML',
  '1005': 'Authentication Error: API-Key empty',
  '1006': 'Authentication Error: API-Key invalid',
  '1007': 'Authentication Error: Password empty',
  '1008': 'Authentication fail',
  '1009': 'No recipients found',
  '1010': 'Invalid Recipient(s)',
  '1011': 'Message body empty',
  '1012': 'Message body exceeds maximum message length',
  '1013': 'Message body contains invalid characters',
  '1014': 'There were duplicates found',
  '1015': 'Authentication Error: IP address not allowed',
  '1016': 'Invalid message id',
  '1017': 'Insufficient credits',
  '1018': 'Account suspended',
  '1019': 'Account deactivated'
  }


def send_sms(msg, recipients, msg_id=None, reply_url=None):
    if msg is None or unicode(msg).strip() == '':
        raise AMSendError("msg cannot be blank")

    if isinstance(recipients, (list, tuple)) and len(recipients) == 0:
        raise AMSendError("supply at least one recipient")

    sms = ET.Element("sms")
    element = ET.SubElement(sms, "api-key")
    element.text = unicode(API_KEY)
    element = ET.SubElement(sms, "password")
    element.text = unicode(API_PASSWORD)
    recipients_element = ET.SubElement(sms, "recipients")
    element = ET.SubElement(sms, "msg")
    element.text = unicode(msg).strip()
    element = ET.SubElement(sms, "concat")
    element.text = "1"
    element = ET.SubElement(sms, "allow_duplicates")
    element.text = unicode(ALLOW_DUPLICATES)
    element = ET.SubElement(sms, "allow_invalid_numbers")
    element.text = unicode(ALLOW_INVALID_NUMBERS)

    if msg_id:
        element = ET.SubElement(sms, "message_id")
        element.text = unicode(msg_id)

    if reply_url:
        element = ET.SubElement(sms, "reply_path")
        element.text = unicode(reply_url)

    # add msisdns to xml
    if isinstance(recipients, (list, tuple)):
        for msisdn in recipients:
            element = ET.SubElement(recipients_element, "mobile")
            element.text = unicode(msisdn)
    else:
        element = ET.SubElement(recipients_element, "mobile")
        element.text = unicode(recipients)

    #print ET.tostring(sms)
    # prepare message ready to sent
    #data = urllib.quote(ET.tostring(sms))
    data = ET.tostring(sms)

    headers = {
        'User-Agent': USER_AGENT,
        'Content-Type': 'text/xml'
    }
    # Send Msg27836805077
    req = urllib2.Request(SMS_API_URL, data, headers)
    resp = urllib2.urlopen(req)

    response = {'status': None, 'msg': None}

    dom = ET.fromstring(resp.read())
    msg_status = dom.find("status").text

    response['status'] = msg_status
    response['msg'] = MSG_CODES[msg_status]

    # Check for invalid numbers
    d = dom.find("invalid_numbers")
    if d is not None:
        invalid_numbers = []
        for m in d.findall("mobile"):
            invalid_numbers.append(m.text)
        response['invalid_numbers'] = invalid_numbers

    # check for duplicates
    d = dom.find("duplicates")
    if d is not None:
        duplicates = []
        for m in d.findall("mobile"):
            duplicates.append(m.text)
        response['duplicates'] = duplicates

    return response


class AMSendError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

# setup a basic test script
if __name__ == '__main__':
    print send_sms(
            'Hello World! This is a Test Message & >< !@#$%^&*()',
            [27834002042]
    )

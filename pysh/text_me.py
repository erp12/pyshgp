from __future__ import absolute_import, division, print_function, unicode_literals

# Download the twilio-python library from http://twilio.com/docs/libraries
import json
import sys
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient
import requests

path_to_json = ""
if sys.version_info[0] == 3:
    path_to_json = input("Path to Twilio JSON:")
else: # Python 2
    path_to_json = raw_input("Path to Twilio JSON:")

if path_to_json == "":
	raise Exception("If you don't want to receive SMS messages, disable all SMS related parameters.")


# Find these values at https://twilio.com/user/account
twilio_json = None
with open(path_to_json) as f:
	twilio_json = json.load(f)
account_sid = twilio_json['account_sid']
auth_token = twilio_json['auth_token']
to = twilio_json['send_to']
from_ = twilio_json['twilio_number']
client = TwilioRestClient(account_sid, auth_token)

def send_text_msg(body):
	try:
		message = client.messages.create(to=to, from_=from_, body=body)
	except TwilioRestException as e:
	    print(e)

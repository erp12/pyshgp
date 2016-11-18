from __future__ import absolute_import, division, print_function, unicode_literals

# Download the twilio-python library from http://twilio.com/docs/libraries
import json
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient
import requests


# Find these values at https://twilio.com/user/account
twilio_json = None
with open('/Users/mm94978/Google_Drive/Research/pysh/pysh/text_me.json') as f:
	twilio_json = json.load(f)
account_sid = twilio_json['account_sid']
auth_token = twilio_json['auth_token']
to = twilio_json['send_to']
from_ = twilio_json['twilio_number']
client = TwilioRestClient(account_sid, auth_token)

print()
print(twilio_json)
print()

def send_text_msg(body):
	try:
		message = client.messages.create(to=to, from_=from_,
	                                     body=body)
	except TwilioRestException as e:
	    print(e)

send_text_msg("Test")
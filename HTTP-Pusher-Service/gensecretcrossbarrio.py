#!/bin/python
import json
import hmac
import hashlib
import base64
import random
from datetime import datetime
import urllib
from httplib import HTTPConnection


def _utcnow():
   """
   Get current time in UTC as ISO 8601 string.
   :returns str -- Current time as string in ISO 8601 format.
   """
   now = datetime.utcnow()
   return now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"




connection = HTTPConnection("127.0.0.1",
               5555, timeout = 30)

endpoint = dict();

endpoint['headers'] = {
         "Content-type": "application/json",
         "User-agent": "crossbarconnect-python"
}
event=dict();
event = {
         'topic': "com.tridas.statemachine.statechange"
      }

#if 'options' in kwargs:
#   event['options'] = kwargs.pop('options')
#   assert(type(event['options']) == dict)

#if args:
event['args'] = {'test': 'funziona'}

#if kwargs:
#   event['kwargs'] = kwargs

try:
   body = json.dumps(event, separators = (',',':'))
   body = body.encode('utf8')
   
except Exception as e:
   raise Exception("invalid event payload - not JSON serializable: {0}".format(e))
seq = 1
params = {
   'timestamp': "2015-03-24T15:38:12.589Z",#_utcnow(),
   'seq': seq,
}


## if the request is to be signed, create extra fields and signature
params['key'] = "test"
params['nonce'] = 10  #random.randint(0, 2^53)

# HMAC[SHA256]_{secret} (key | timestamp | seq | nonce | body) => signature



hm = hmac.new("kkjH68GiuUZ".encode('utf8'), None, hashlib.sha256)
print("1-->"+hm.hexdigest());

hm.update(params['key'].encode('utf8'))
print("2-->"+hm.hexdigest());

hm.update(params['timestamp'].encode('utf8'))
print("3-->"+hm.hexdigest());

hm.update(u"{0}".format(params['seq']).encode('utf8'))
print("4-->"+hm.hexdigest());


hm.update(u"{0}".format(params['nonce']).encode('utf8'))
print("5:-->"+hm.hexdigest());


hm.update(body)
print("final-->"+hm.hexdigest());

print(body)

signature = base64.urlsafe_b64encode(hm.digest())

params['signature'] = signature
print(params)
seq += 1

path = "{0}?{1}".format("http://127.0.0.1:5555", urllib.urlencode(params))
print(path)
## now issue the HTTP/POST
##
connection.request('POST', path, body, endpoint['headers'])
response = connection.getresponse()
response_body = response.read()

print(response)

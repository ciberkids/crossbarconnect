###############################################################################
##
##  Copyright (C) 2012-2014 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################


import json, datetime, hmac, hashlib, base64

from six.moves.urllib import parse
from six.moves.http_client import HTTPConnection



class Client:
   """
   Crossbar.io push client.
   """

   def __init__(self, pushEndpoint, authKey = None, authSecret = None, timeout = 5):
      """
      Create a new Crossbar.io push client.

      The only mandatory argument is the Push service endpoint of the Crossbar.io
      instance to push to.

      For signed pushes, provide authentication key and secret. If those are not
      given, unsigned pushes are performed.

      :param pushEndpoint: Push service endpoint of Crossbar.io.
      :type pushEndpoint: str
      :param authKey: Optional authentication key to use.
      :type authKey: str
      :param authSecret: When using an authentication key, the corresponding authencation secret.
      :type authSecret: str
      :param timeout: Timeout for pushes to WebMQ.
      :type timeout: int
      """
      if authKey or authSecret:
         if not (authKey and authSecret):
            raise Exception("either authKey and authSecret must both be given, or none at all")
      self.authKey = authKey
      self.authSecret = authSecret
      self.pushEndpoint = self._parsePushUrl(pushEndpoint)
      self.pushEndpoint['headers'] = {"Content-type": "application/x-www-form-urlencoded",
                                      "User-agent": "crossbarconnect-python"}

      if self.pushEndpoint['secure']:
         raise Exception("Push via HTTPS not implemented")
      self.pushConnection = HTTPConnection(self.pushEndpoint['host'],
                                           self.pushEndpoint['port'],
                                           timeout = timeout)


   def push(self, topic, event, eligible = None, exclude = None):
      """
      Push event to subscribers on specified topic via Crossbar.io.

      The event can be of any simple type or complex object that can
      be serialized to JSON.

      :param topic: Topic to push to. Must be a valid URI from the HTTP scheme.
      :type topic: str
      :param event: Event to push. Must be JSON-serializable.
      :type event: obj
      :param eligible: Optional list of WAMP session IDs eligible to receive this event.
      :type eligible: list of strings
      :param exclude: Optional list of WAMP session IDs to exclude from receivers.
      :type exclude: list of strings
      """
      try:
         msg = json.dumps(event)
      except Exception as e:
         raise Exception("invalid event object - not JSON serializable (%s)" % str(e))

      params = {'topic': topic}
      params.update(self._signature(topic, msg))
      if eligible:
         params['eligible': ','.join(eligible)]
      if exclude:
         params['exclude': ','.join(exclude)]
      path = "%s?%s" % (parse.quote(self.pushEndpoint['path']), parse.urlencode(params))

      self.pushConnection.request('POST', path, msg, self.pushEndpoint['headers'])
      response = self.pushConnection.getresponse()
      data = response.read()
      if response.status != 202:
         raise Exception("Push failed %d [%s] - %s" % (response.status, response.reason, data))


   def _utcnow(self):
      now = datetime.datetime.utcnow()
      return now.strftime("%Y-%m-%dT%H:%M:%SZ")


   def _signature(self, topic, body):
      if self.authKey:
         # HMAC[SHA256]_{authSecret}(topic | authKey | timestamp | body) => appsig
         timestamp = self._utcnow()
         hm = hmac.new(self.authSecret, None, hashlib.sha256)
         hm.update(topic)
         hm.update(self.authKey)
         hm.update(timestamp)
         hm.update(body)
         sig = base64.urlsafe_b64encode(hm.digest())
         return {'timestamp': timestamp,
                 'appkey': self.authKey,
                 'signature': sig}
      else:
         return {}


   def _parsePushUrl(self, url):
      parsed = parse.urlparse(url)
      if parsed.scheme not in ["http", "https"]:
         raise Exception("invalid Push URL scheme '%s'" % parsed.scheme)
      if parsed.port is None or parsed.port == "":
         if parsed.scheme == "http":
            port = 80
         elif parsed.scheme == "https":
            port = 443
         else:
            raise Exception("logic error")
      else:
         port = int(parsed.port)
      if parsed.fragment is not None and parsed.fragment != "":
         raise Exception("invalid Push URL: non-empty fragment '%s" % parsed.fragment)
      if parsed.query is not None and parsed.query != "":
         raise Exception("invalid Push URL: non-empty query string '%s" % parsed.query)
      if parsed.path is not None and parsed.path != "":
         ppath = parsed.path
         path = parse.unquote(ppath)
      else:
         ppath = "/"
         path = ppath
      return {'secure': parsed.scheme == "https",
              'host': parsed.hostname,
              'port': port,
              'path': path}

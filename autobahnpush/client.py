###############################################################################
##
##  Copyright 2012 Tavendo GmbH
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

import json, httplib, urlparse, urllib, datetime, hmac, hashlib, base64


class Client:
   """
   Autobahn.ws WebSocket Appliance Push client.
   """

   def __init__(self, pushto, appkey = None, appsecret = None, timeout = 5):
      """
      Create Push API client.
      """
      if appkey or appsecret:
         if not (appkey and appsecret):
            raise Exception("either appkey and appsecret must both be given, or none at all")
      self.appkey = appkey
      self.appsecret = appsecret
      self.pushEndpoint = self._parsePushUrl(pushto)
      self.pushEndpoint['headers'] = {"Content-type": "application/x-www-form-urlencoded",
                                      "User-agent": "AutobahnPushPython"}

      if self.pushEndpoint['secure']:
         raise Exception("https Push URL not implemented")
      self.pushConnection = httplib.HTTPConnection(self.pushEndpoint['host'],
                                                   self.pushEndpoint['port'],
                                                   timeout = timeout)


   def push(self, topic, event, eligible = None, exclude = None):
      """
      Push message view Autobahn.ws WebSocket Appliance.
      """
      try:
         msg = json.dumps(event)
      except Exception, e:
         raise Exception("invalid event object - not JSON serializable (%s)" % str(e))

      params = {'topicuri': topic}
      params.update(self._signature(topic, msg))
      if eligible:
         params['eligible': ','.join(eligible)]
      if exclude:
         params['exclude': ','.join(exclude)]
      path = "%s?%s" % (urllib.quote(self.pushEndpoint['path']), urllib.urlencode(params))

      self.pushConnection.request('POST', path, msg, self.pushEndpoint['headers'])
      response = self.pushConnection.getresponse()
      data = response.read()
      if response.status != 202:
         raise Exception("Push failed %d [%s] - %s" % (response.status, response.reason, data))


   def _utcnow(self):
      now = datetime.datetime.utcnow()
      return now.strftime("%Y-%m-%dT%H:%M:%SZ")


   def _signature(self, topic, body):
      if self.appkey:
         # HMAC[SHA1]_{appsecret}(topicuri | appkey | timestamp | body) => appsig
         timestamp = self._utcnow()
         hm = hmac.new(self.appsecret, None, hashlib.sha1)
         hm.update(topic)
         hm.update(self.appkey)
         hm.update(timestamp)
         hm.update(body)
         sig = base64.urlsafe_b64encode(hm.digest())
         return {'timestamp': timestamp,
                 'appkey': self.appkey,
                 'signature': sig}
      else:
         return {}


   def _parsePushUrl(self, url):
      parsed = urlparse.urlparse(url)
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
         path = urllib.unquote(ppath)
      else:
         ppath = "/"
         path = ppath
      return {'secure': parsed.scheme == "https",
              'host': parsed.hostname,
              'port': port,
              'path': path}

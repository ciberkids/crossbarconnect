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

import sys
import autobahnpush


if __name__ == '__main__':

   if len(sys.argv) < 2:
      print "Usage: python __init__.py <Autobahn.ws Push Endpoint>"
      print "  i.e. python __init__.py http://192.168.1.135:8080"
      sys.exit(1)

   ## push 5 messages
   ##
   client = autobahnpush.Client(sys.argv[1])
   for i in xrange(5):
      client.push(topic = "http://example.com/topic1",
                  event = {'i': i, 'msg': "Hello from Python %d!!" % i})
      print "message %d pushed!" % i

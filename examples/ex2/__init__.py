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
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def index():
   """
   """
   return render_template('index.html')


@app.route("/client")
def client():
   """
   Render a real-time WebSocket client receiving data from Autobahn.ws
   message broker.
   """
   return render_template('client.html', server = sys.argv[1])


@app.route('/form1')
def form1():
   """
   Render a HTML form.
   """
   return render_template('form1.html', name = "Heinzelmann", age = 23)


@app.route('/submit1', methods = ['POST'])
def submit1():
   """
   Receive data from a submitted HTML form and forward data to
   WebSocket clients by using the Autobahn.ws Push API.
   """
   client = autobahnpush.Client(sys.argv[2])
   try:
      client.push(topic = "http://example.com/topic1",
                  event = {'name': request.form['name'],
                           'age': request.form['age']})
      return "Push succeeded"
   except Exception, e:
      return "Push failed: %s" % e


if __name__ == "__main__":

   if len(sys.argv) < 3:
      print "Usage: python __init__.py <Autobahn.ws WebSocket Endpoint> <Autobahn.ws Push Endpoint>"
      print "  i.e. python __init__.py ws://192.168.1.135:80            http://192.168.1.135:8080"
      sys.exit(1)

   app.run(debug = True)

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
import webmqconnect
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def index():
   """
   Render the demo main page.
   """
   return render_template('index.html')


@app.route("/client")
def client():
   """
   Render a Real-time client connecting to Tavendo WebMQ via WebSocket/WAMP.
   """
   return render_template('client.html', server = sys.argv[1], topic = sys.argv[3])


@app.route('/form1')
def form1():
   """
   Render a HTML form.
   """
   return render_template('form1.html', name = "Heinzelmann", age = 23)


@app.route('/submit1', methods = ['POST'])
def submit1():
   """
   Receive data from a submitted HTML form and push data to Tavendo WebMQ.
   """
   client = webmqconnect.Client(sys.argv[2])
   try:
      client.push(topic = sys.argv[3],
                  event = {'name': request.form['name'],
                           'age': request.form['age']})
      return "Push succeeded"
   except Exception, e:
      return "Push failed: %s" % e


if __name__ == "__main__":

   if len(sys.argv) < 4:
      print """
Usage:   python __init__.py <WebMQ WebSocket Endpoint> <WebMQ Push Endpoint> <Topic URI>
Example: python __init__.py wss://autobahn-euwest.tavendo.de http://autobahn-euwest.tavendo.de:8080 http://autobahn.tavendo.de/public/demo/foobar1
"""
      sys.exit(1)

   app.run(debug = True)

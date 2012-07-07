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

from setuptools import setup

LONGDESC = """
Tavendo WebMQ Web Message Broker extends existing Web applications to the
Real-time Web.

This module provides the connector to integrate Python-based Web applications
written for popular frameworks like Django, Flask and others with Tavendo WebMQ.

Using this connector, you can push events from your Web app (or a plain Python
script) to Tavendo WebMQ which will then forward the event to all real-time
clients connected and subscribed to the topic you push to.

For more information, please visit

   * http://www.tavendo.de/webmq
   * https://github.com/tavendo/WebMQConnectPython
"""

setup(
   name = 'webmqconnect',
   version = '0.4.0',
   description = 'Tavendo WebMQ Connect for Python',
   long_description = LONGDESC,
   license = 'Apache License 2.0',
   author = 'Tavendo GmbH',
   url = 'http://www.tavendo.de/webmq',
   platforms = ('Any'),
   install_requires = ['setuptools'],
   packages = ['webmqconnect'],
   package_data = {'': ['LICENSE']},
   zip_safe = False,
   classifiers = ["License :: OSI Approved :: Apache Software License",
                  "Development Status :: 4 - Beta",
                  "Environment :: Console",
                  "Intended Audience :: Developers",
                  "Operating System :: OS Independent",
                  "Programming Language :: Python",
                  "Topic :: Internet :: WWW/HTTP",
                  "Topic :: Software Development :: Libraries"],
   keywords = 'webmq websocket realtime push rest'
)

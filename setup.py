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
The Autobahn.ws WebSocket Appliance has an embedded REST API which you can
use to push out messages to WebSocket clients such as browsers connected
to the appliance.

This module provides a convenient client to perform the simple HTTP/POSTs
which the REST API consumes.

The module has no external dependencies and is very simple to use.
"""

setup(
   name = 'autobahnpush',
   version = '0.3',
   description = 'Autobahn.ws Push for Python.',
   long_description = LONGDESC,
   license = 'Apache License 2.0',
   author = 'Tavendo GmbH',
   author_email = 'autobahnws@googlegroups.com',
   url = 'http://autobahn.ws',
   platforms = ('Any'),
   install_requires = ['setuptools'],
   packages = ['autobahnpush'],
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
   keywords = 'autobahn autobahn.ws websocket realtime push rest'
)

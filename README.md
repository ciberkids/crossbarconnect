Autobahn.ws Push for Python.
============================

What is that?
-------------

The Autobahn.ws WebSocket Appliance <http://autobahn.ws> has an embedded
REST API which you can use to push out messages to WebSocket clients
such as browsers connected to the appliance.

This module provides a convenient client to perform the simple HTTP/POSTs
which the REST API consumes.

The module has no external dependencies and is very simple to use.



Installation
------------

The module has no external dependencies and has been tested on Python 2.7.

To install, the most convenient way is by using the Python package management
tools `easy_install` or `pip`.

For example:

    easy_install install autobahnpush



Pushing
-------

Pushing from Python is as simple as 2 lines:


    import autobahnpush

    client = autobahnpush.Client("<Your Autobahn.ws Appliance Push URL>")
    client.push(topic = "<Your publication topic URI>",
                event = {'field1': "Your published event.", ...})


Basically, you create a client providing the Push endpoint URL served
by your appliance instance.

Then you reuse that client for pushing once or multiple times.
Doing so, you provide the topic to publish under, and the event you
want to publish. The event can be any Python object that can be
serialized to JSON.


Signed Pushes
-------------

For production setups you may have your Autobahn.ws appliance configured
so that it only accepts _signed_ pushes.

    client = autobahnpush.Client("<Your Autobahn.ws Appliance Push URL>",
                                 appkey = "<Your App Key>",
                                 appsecret = "<Your App Secret>")


Advanced Options
----------------

You can exclude specific WebSocket clients from receiving your pushed
message, even though they may be subscribed to the topic you are
pushing to:

    client.push(..., exclude = [<list of session IDs>])

You can also specify a whitelist of WebSocket clients

    client.push(..., eligible = [<list of session IDs>])



Copyright
---------

Autobahn.ws - The WebSockets Appliance.
Copyright (c) 2012 Tavendo GmbH.
Licensed under the Apache 2.0 License.
See license text under LICENSE.

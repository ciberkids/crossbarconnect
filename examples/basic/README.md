Using WebMQ Connect for Python from Scripts
===========================================

This example demonstrates how to use *WebMQ Connect for Python* from
Python command line scripts.

Running
-------

To run, open a command shell and

	python push.py <WebMQ Push Endpoint> <Topic URI> <Message>

where

	<WebMQ Push Endpoint> : Push Service Endpoint of your WebMQ appliance
	<Topic URI>           : Topic URI you want to push to
    <Message>             : Message you want to push    

For example:

	python push.py http://autobahn-euwest.tavendo.de:8080 http://autobahn.tavendo.de/public/demo/pubsub/577274 "Hello from Python"

You can use our public demo on

	http://www.tavendo.de/webmq/demos/pubsub

to see messages arriving in your browser. Adjust the server and topic to those shown in the demo.

Signed Pushes
-------------

To do signed pushes, open a command shell and

	python push.py <WebMQ Push Endpoint> <Auth/App Key> <Auth/App Secret> <Topic URI> <Message>

where

	<WebMQ Push Endpoint> : Push Service Endpoint of your WebMQ appliance
    <Auth/App Key>        : The authentication key = application key configured in WebMQ.
    <Auth/App Secret>     : The secret corrsponding to the key.
	<Topic URI>           : Topic URI you want to push to
    <Message>             : Message you want to push    

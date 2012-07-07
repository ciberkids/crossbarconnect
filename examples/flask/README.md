Using WebMQ Connect for Python with Flask
=========================================

This example shows how you can use **WebMQ Connect for Python** from dynamic
web applications based on the [Flask](http://flask.pocoo.org).

Running
-------

Start the web application by

	cd examples/flask
	python __init__.py <WebSocket Endpoint> <Push Endpoint> <Topic URI>

where

	<WebSocket Endpoint> : WebSocket Service Endpoint of your WebMQ appliance
	<Push Endpoint>      : Push Service Endpoint of your WebMQ appliance
	<Topic URI>          : Topic URI you want to use


For example

	python __init__.py wss://autobahn-euwest.tavendo.de http://autobahn-euwest.tavendo.de:8080 http://autobahn.tavendo.de/public/demo/foobar1


Now open

	http://localhost:5000

in your browser, and continue opening the WebSocket client in one browser window and the HTML form in another.

Submit form data and see how data is received in real-time in the WebSocket client window.


How it works
------------

When the HTML form is submitted, we receive the submitted data in Flask. At this point we create a **WebMQ Connect** client and push the data to WebMQ.

Tavendo WebMQ will dispatch the received data to all clients subscribed to the topic specified in the push.

The WebSocket client uses **AutobahnJS** to open a WAMP session to Tavendo WebMQ, subscribes to interesting topics, and receives data.
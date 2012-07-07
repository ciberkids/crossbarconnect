Using WebMQ Connect for Python from Scripts
===========================================

This example demonstrates how to use *WebMQ Connect for Python* from
Python command line scripts.

To run, open a command shell and

	python push.py <Tavendo WebMQ Push URL> <Topic URI> <Message>

where **Tavendo WebMQ Push URL** is the Push URL of your WebMQ appliance, **Topic URI** is the topic you want to push to and **Message** is the message text you want to push.

For example:

	python push.py http://autobahn-euwest.tavendo.de:8080 http://autobahn.tavendo.de/public/demo/pubsub/577274 "Hello from Python"

You can use our public demo on

	http://www.tavendo.de/webmq/demos/pubsub

to see messages arriving in your browser. Adjust the server and topic to those shown in the demo.
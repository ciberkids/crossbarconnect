# Pushing Events - Basic Example

This example demonstrates how to push real-time notifications to Web clients using the HTTP bridge built into Crossbar.io.

The [test.py](test.py) script creates a new Crossbar.io pusher client

```python
client = crossbarconnect.Client("http://127.0.0.1:8080/push")
```

and uses this to submit events to be distributed by Crossbar.io to WAMP clients in real-time:

```python
client.push(topic = "com.myapp.topic1", event = {'seq': i, 'msg': "Hello, world!"})
```

Under the hood, `crossbarconnect.Client.push` will prepare and issue a HTTP/POST request to the Crossbar.io HTTP bridge.

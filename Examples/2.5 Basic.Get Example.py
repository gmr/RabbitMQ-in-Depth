#!/usr/bin/env python

# Import the RabbitMQ Client Library
import rabbitpy

# The URL to connect to
url = 'amqp://guest:guest@localhost:5672/%2F'

# Open a connection to RabbitMQ
connection = rabbitpy.Connection(url)

# Open a channel to communicate with RabbitMQ on
channel = connection.channel()

# Create an object for interacting with the queue
queue = rabbitpy.Queue(channel, 'example')

# While there are messages in the queue, fetch them using Basic.Get
while len(queue) > 0:
    message = queue.get()
    print('Message:')
    print(' ID: %s' % message.properties['message_id'])
    print(' Time: %s' % message.properties['timestamp'].isoformat())
    print(' Body: %s' % message.body)
    message.ack()

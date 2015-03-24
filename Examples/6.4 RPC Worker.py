import os
import rabbitpy
import time
from ch6 import detect
from ch6 import utils

# Open the connection and the channel
connection = rabbitpy.Connection()
channel = connection.channel()

# Create the worker queue
queue_name = 'rpc-worker-%s' % os.getpid()
queue = rabbitpy.Queue(channel, queue_name,
                       auto_delete=True,
                       durable=False,
                       exclusive=True)

# Declare the worker queue
if queue.declare():
    print('Worker queue declared')

# Bind the worker queue
if queue.bind('headers-rpc-requests',
              arguments={'x-match': 'all',
                         'source': 'profile',
                         'object': 'image',
                         'action': 'new'}):
    print('Worker queue bound')

# Consume messages from RabbitMQ
for message in queue.consume_messages():

    # Display how long it took for the message to get here
    duration = time.time() - int(message.properties['timestamp'].strftime('%s'))
    print('Received RPC request published %.2f seconds ago' % duration)

    # Write out the message body to a temp file for facial detection process
    temp_file = utils.write_temp_file(message.body,
                                      message.properties['content_type'])

    # Detect faces
    result_file = detect.faces(temp_file)

    # Build response properties including the timestamp from the first publish
    properties = {'app_id': 'Chapter 6 Listing 2 Consumer',
                  'content_type': message.properties['content_type'],
                  'correlation_id': message.properties['correlation_id'],
                  'headers': {
                      'first_publish': message.properties['timestamp']}}

    # The result file could just be the original image if nothing detected
    body = utils.read_image(result_file)

    # Remove the temp file
    os.unlink(temp_file)

    # Remove the result file
    os.unlink(result_file)

    # Publish the response response
    response = rabbitpy.Message(channel, body, properties, opinionated=True)
    response.publish('rpc-replies', message.properties['reply_to'])

    # Acknowledge the delivery of the RPC request message
    message.ack()

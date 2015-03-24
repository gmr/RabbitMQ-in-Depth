import os
import hashlib
import rabbitpy

# Create the worker queue
queue_name = 'hashing-worker-%s' % os.getpid()
queue = rabbitpy.Queue(channel, queue_name,
                       auto_delete=True,
                       durable=False,
                       exclusive=True)

# Declare the worker queue
if queue.declare():
    print('Worker queue declared')

# Bind the worker queue
if queue.bind('fanout-rpc-requests'):
    print('Worker queue bound')

# Consume messages from RabbitMQ
for message in queue.consume_messages():

    # Create the hashing object
    hash_obj = hashlib.md5(message.body)

    # Print out the info, this might go into a database or log file
    print('Image with correlation-id of %s has a hash of %s' %
          (message.properties['correlation_id'],
           hash_obj.hexdigest()))

    # Acknowledge the delivery of the RPC request message
    message.ack()

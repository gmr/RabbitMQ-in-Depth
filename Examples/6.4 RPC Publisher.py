import os
import rabbitpy
import time
from ch6 import utils

# Open the channel and connection
connection = rabbitpy.Connection()
channel = connection.channel()

# Create the response queue that will automatically delete, is not durable and
# is exclusive to this publisher
queue_name = 'response-queue-%s' % os.getpid()
response_queue = rabbitpy.Queue(channel,
                                queue_name,
                                auto_delete=True,
                                durable=False,
                                exclusive=True)
# Declare the response queue
if response_queue.declare():
    print('Response queue declared')

# Bind the response queue
if response_queue.bind('rpc-replies', queue_name):
    print('Response queue bound')

# Iterate through the images to send RPC requests for
for img_id, filename in enumerate(utils.get_images()):

    print('Sending request for image #%s: %s' % (img_id, filename))

    # Create the message
    message = rabbitpy.Message(channel,
                               utils.read_image(filename),
                               {'content_type': utils.mime_type(filename),
                                'correlation_id': str(img_id),
                                'headers': {'source': 'profile',
                                            'object': 'image',
                                            'action': 'new'},
                                'reply_to': queue_name},
                               opinionated=True)

    # Pubish the message
    message.publish('headers-rpc-requests')

    # Loop until there is a response message
    message = None
    while not message:
        time.sleep(0.5)
        message = response_queue.get()

    # Ack the response message
    message.ack()

    # Caculate how long it took from publish to response
    duration = (time.time() -
                time.mktime(message.properties['headers']['first_publish']))

    print('Facial detection RPC call for image %s total duration: %s' %
          (message.properties['correlation_id'], duration))

    # Display the image in the IPython notebook interface
    utils.display_image(message.body, message.properties['content_type'])

print('RPC requests processed')

# Close the channel and connection
channel.close()
connection.close()

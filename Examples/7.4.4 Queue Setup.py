import rabbitpy

with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        queue = rabbitpy.Queue(channel, 'statelessd-messages')
        queue.declare()
        queue.bind('amq.topic', '#')

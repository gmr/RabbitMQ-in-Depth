import rabbitpy

connection = rabbitpy.Connection()
try:
    with connection.channel() as channel:
        arguments = {'x-ha-policy': 'nodes',
                     'x-ha-nodes': ['rabbit@node1',
                                    'rabbit@node2',
                                    'rabbit@node3']}
        queue = rabbitpy.Queue(channel,
                               'my-2nd-ha-queue',
                               arguments=arguments)
        if queue.declare():
            print('Queue declared')
except rabbitpy.exceptions.RemoteClosedChannelException as error:
    print('Queue declare failed: %s' % error)

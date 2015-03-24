import rabbitpy

connection = rabbitpy.Connection()
try:
    with connection.channel() as channel:
        queue = rabbitpy.Queue(channel,
                               'my-ha-queue',
                               arguments={'x-ha-policy': 'all'})
        if queue.declare():
            print('Queue declared')
except rabbitpy.exceptions.RemoteClosedChannelException as error:
    print('Queue declare failed: %s' % error)

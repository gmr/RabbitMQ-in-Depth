import rmqid

connection = rmqid.Connection()                                    #A
try:
    with connection.channel() as channel:                          #B
        arguments = {'x-ha-policy': 'nodes',                       #C
                     'x-ha-nodes': ['rabbit@node1',
                                    'rabbit@node2',
                                    'rabbit@node3']}
        queue = rmqid.Queue(channel,                               #D
                            'my-ha-queue',               
                            arguments=arguments)
        if queue.declare():                                        #E
            print('Queue declared')
except rmqid.exceptions.RemoteClosedChannelException as error:     #F
    print('Queue declare failed: %s' % error)

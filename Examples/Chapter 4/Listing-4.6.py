import rmqid

connection = rmqid.Connection()                                    #A
try:
    with connection.channel() as channel:                          #B
        queue = rmqid.Queue(channel,                               #C
                            'my-ha-queue',               
                            arguments={'x-ha-policy': 'all'})
        if queue.declare():                                        #D
            print('Queue declared')
except rmqid.exceptions.RemoteClosedChannelException as error:     #E
    print('Queue declare failed: %s' % error)

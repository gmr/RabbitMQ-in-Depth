import rmqid

url = 'amqp://guest:guest@localhost:5672/%2f'             
with rmqid.Connection(url) as connection:                          #A
    with connection.channel() as channel:                          #B
        queue = rmqid.Queue(channel, 'durable-queue', 
                            durable=True)                          #C
        if queue.declare():                                        #D
            print 'Queue declared'                                 #E 

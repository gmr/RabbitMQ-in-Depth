import rmqid

url = 'amqp://guest:guest@localhost:5672/%2f'                      
with rmqid.Connection(url) as connection:                          #A
    with connection.channel() as channel:                          #B
    
        my_ae = rmqid.Exchange(channel,                            #C
                               'my-ae',
                               exchange_type='fanout')   
        my_ae.declare()                                            #D

        args = {'alternate-exchange': my_ae.name}                  #E
        
        exchange = rmqid.Exchange(channel,                         #F 
                                  'graphite', 
                                  exchange_type='topic',                    
                                  arguments=args) 
        exchange.declare()                                         #G

        queue = rmqid.Queue(channel, 'unroutable-messages')        #H
        queue.declare()                                            #I
        if queue.bind(my_ae, '#'):                                 #J
            print('Queue bound to alternate-exchange')

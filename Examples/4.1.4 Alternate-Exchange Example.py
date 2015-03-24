import rabbitpy

with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        my_ae = rabbitpy.Exchange(channel, 'my-ae',
                                  exchange_type='fanout')
        my_ae.declare()
        args = {'alternate-exchange': my_ae.name}
        exchange = rabbitpy.Exchange(channel,
                                     'graphite',
                                     exchange_type='topic',
                                     arguments=args)
        exchange.declare()
        queue = rabbitpy.Queue(channel, 'unroutable-messages')
        queue.declare()
        if queue.bind(my_ae, '#'):
            print('Queue bound to alternate-exchange')

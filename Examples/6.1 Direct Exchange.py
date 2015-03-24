import rabbitpy

with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        exchange = rabbitpy.Exchange(channel, 'direct-example',
                                     exchange_type='direct')
        exchange.declare()

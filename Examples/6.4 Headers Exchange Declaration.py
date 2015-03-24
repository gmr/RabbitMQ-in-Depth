import rabbitpy

with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        exchange = rabbitpy.Exchange(channel,
                                     'headers-rpc-requests',
                                     exchange_type='headers')
        exchange.declare()

import rabbitpy

with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        exchange = rabbitpy.Exchange(channel, 'image-storage',
                                     exchange_type='x-consistent-hash',
                                     arguments={'hash-header': 'image-hash'})
        exchange.declare()

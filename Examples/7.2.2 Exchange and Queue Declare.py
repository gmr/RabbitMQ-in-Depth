import rabbitpy

with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        exchange = rabbitpy.Exchange(channel, 'stomp-routing')
        exchange.declare()
        queue = rabbitpy.Queue(channel, 'bound-queue',
                               arguments={'x-max-length': 10})
        queue.declare()
        queue.bind(exchange, 'example')

import rabbitpy

with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        queue = rabbitpy.Queue(channel, 'exclusive-example',
                               exclusive=True)
        queue.declare()

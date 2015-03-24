import rabbitpy

with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        queue = rabbitpy.Queue(channel, 'max-length-queue',
                               arguments={'x-max-length': 1000})
        queue.declare()

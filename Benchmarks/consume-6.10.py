import logging
import sys
import rabbitpy
import time

with rabbitpy.Connection() as connection:
    with connection.channel() as channel:

        print('Declaring and the queue')
        queue = rabbitpy.Queue(channel,
                               'benchmark_queue',
                               durable=False,
                               arguments={'x-message-ttl': 300000})
        queue.declare()

        print('Consuming')
        for message in queue.consume_messages(True):
            sys.stdout.write('.')

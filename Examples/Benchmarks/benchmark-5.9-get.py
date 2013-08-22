import logging
import rmqid
import time

ROUTING_KEY = 'benchmark_get'
ITERATIONS = 100000

logging.basicConfig(level=logging.INFO)

with open('lorem.txt') as handle:
    BODY = handle.read()

logging.info('Starting benchmark')
with rmqid.Connection() as connection:
    with connection.channel() as channel:
        queue = rmqid.Queue(channel, ROUTING_KEY,
                            auto_delete=True, exclusive=True)
        queue.declare()
        logging.info('Queue declared, publishing %i messages', ITERATIONS)
        for iteration in range(0, ITERATIONS):
            message = rmqid.Message(channel, BODY[:2048],
                                    {'content_type': 'text/plain',
                                     'delivery_mode': 1})
            message.publish('', ROUTING_KEY)

        received = 0
        start_time = time.time()
        while received < ITERATIONS:
            message = queue.get(acknowledge=False)
            #message.ack()
            received += 1

total_time = time.time() - start_time
velocity = float(ITERATIONS / total_time)
logging.info('Get %.2f messages/sec in %.2f seconds', velocity, total_time)

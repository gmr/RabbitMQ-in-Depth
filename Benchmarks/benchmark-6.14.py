import hashlib
import logging
import sys
import rabbitpy
import time

logging.basicConfig(level=logging.DEBUG)

ARGS = {'source': 'profile',
        'object': 'image',
        'action': 'new'}
EXCHANGES = ['topic', 'headers']
ITERATIONS = 3
MESSAGES = 100000
ROUTING_KEY = 'image.profile.new'


def bind_topic(queue):
    print('Binding topic exchange')
    queue.bind('benchmark_topic', 'image.#', arguments={})


def bind_headers(queue):
    print('Binding headers exchange')
    args = dict(ARGS)
    args['x-match'] = 'any'
    queue.bind('benchmark_headers', None, arguments=args)


def declare_exchange(channel, exchange_type):
    print('Creating the %s exchange' % exchange_type)
    exchange = rabbitpy.Exchange(channel,
                                 'benchmark_%s' % exchange_type,
                                 exchange_type)
    exchange.declare()
    return exchange


def unbind_topic(queue):
    print('Unbinding topic exchange')
    queue.bind('benchmark_topic', ROUTING_KEY)


def unbind_headers(queue):
    print('Unbinding headers exchange')
    queue.unbind('benchmark_headers')


with open('results.csv', 'a') as handle:
    handle.write('"Exchange Type","Iteration","Test Size","Duration","Velocity"\n')

all_start = time.time()

print('Declaring and Binding Exchanges')
with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        for exchange_type in EXCHANGES:
            declare_exchange(channel, exchange_type)

print('Performing Benchmark')
with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        queue = rabbitpy.Queue(channel,
                               'benchmark_queue',
                               durable=False,
                               arguments={'x-message-ttl': 300000})
        queue.declare()
        exchange_type = 'headers'
        routing_key = ROUTING_KEY if exchange_type == 'topic' else None
        exchange_name = 'benchmark_%s' % exchange_type

        # Bind the queue
        locals()['bind_%s' % exchange_type](queue)
        print('Publishing %i messages to %s %s' %
              (MESSAGES, exchange_name, routing_key))

        start_time = time.time()
        for msg_num in range(MESSAGES):
            if exchange_type == 'topic':
                msg = rabbitpy.Message(channel,
                                       'Test message #%s' % msg_num)
                msg.publish(exchange_name, routing_key)
            else:
                msg = rabbitpy.Message(channel,
                                       'Test message #%s' % msg_num,
                                       {'headers': ARGS})
                msg.publish(exchange_name)

        duration = time.time() - start_time
        velocity = float(MESSAGES) / float(duration)

        print('Sent %i messages in %.2f seconds (%.2f msg/s)' %
                (MESSAGES, duration, velocity))

        with open('results.csv', 'a') as handle:
            handle.write('"%s",%i,%.2f,%.2f\n' %
                         (exchange_type,
                          MESSAGES, duration, velocity))
        print('Wrote results')

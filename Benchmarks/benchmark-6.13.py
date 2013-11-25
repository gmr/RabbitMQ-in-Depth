import hashlib
import logging
import sys
import rabbitpy
import time


ARGS = {'age': '30',
        'gender': 'male',
        'authenticated': 'true',
        'department': 'Operations',
        'id': '655321'}
EXCHANGES = ['direct', 'fanout', 'topic', 'headers']
SIZES = [0, 20, 40, 60, 80, 100]
ITERATIONS = 3
MESSAGES = 100000
ROUTING_KEY = 'benchmark_test'


def bind_direct(queue):
    print('Binding direct exchange')
    queue.bind('benchmark_direct', ROUTING_KEY)


def unbind_direct(queue):
    print('Unbinding direct exchange')
    queue.unbind('benchmark_direct', ROUTING_KEY)


def bind_fanout(queue):
    print('Binding fanout exchange')
    queue.bind('benchmark_fanout')


def unbind_fanout(queue):
    print('Unbinding fanout exchange')
    queue.unbind('benchmark_fanout')


def bind_topic(queue):
    print('Binding topic exchange')
    queue.bind('benchmark_topic', ROUTING_KEY)


def unbind_topic(queue):
    print('Unbinding topic exchange')
    queue.unbind('benchmark_topic', ROUTING_KEY)


def bind_headers(queue):
    print('Unbinding headers exchange')
    args = dict(ARGS)
    args['x-match'] = 'all'
    queue.bind('benchmark_headers', arguments=args)


def unbind_headers(queue):
    print('Unbinding headers exchange')
    queue.unbind('benchmark_headers')


def declare_exchange(channel, exchange_type):
    print('Creating the %s exchange' % exchange_type)
    exchange = rabbitpy.Exchange(channel,
                                 'benchmark_%s' % exchange_type,
                                 exchange_type)
    exchange.declare()
    return exchange


def declare_queue(channel):
    print('Declaring and the queue')
    queue = rabbitpy.Queue(channel,
                           'benchmark_queue',
                           durable=False,
                           arguments={'x-message-ttl': 300000})
    queue.declare()
    return queue


def build_args(arg_count):
    print('Building args')
    if not arg_count:
        return {}
    args = dict(ARGS)
    for iteration in range(arg_count):
        hash_value = hashlib.md5(str(iteration))
        args['key-%s' % iteration] = str(hash_value.hexdigest())
    return args


with open('results.csv', 'w') as handle:
    handle.write('"Exchange Type","Iteration","Header Table Size",'
                 '"Test Size","Duration","Velocity"\n')

all_start = time.time()

for size in SIZES:
    args = build_args(size)
    for iteration in range(ITERATIONS):
         with rabbitpy.Connection() as connection:
            with connection.channel() as channel:
                queue = declare_queue(channel)

                for exchange_type in EXCHANGES:
                    declare_exchange(channel, exchange_type)

                for exchange_type in EXCHANGES:
                    routing_key = (ROUTING_KEY if exchange_type in ['direct', 'topic']
                                   else None)

                    exchange_name = 'benchmark_%s' % exchange_type
                    locals()['bind_%s' % exchange_type](queue)

                    print('Publishing %i messages to %s %s, pass #%i, headers size %i' %
                             (MESSAGES, exchange_name, routing_key, iteration, len(args.keys())))

                    start_time = time.time()
                    for msg_num in range(MESSAGES):
                        msg = rabbitpy.Message(channel,
                                               'Test message #%s' % msg_num,
                                               {'headers': args})
                        msg.publish(exchange_name, routing_key)

                    duration = time.time() - start_time
                    velocity = float(MESSAGES) / float(duration)

                    print('Sent %i messages in %.2f seconds (%.2f msg/s)' %
                            (MESSAGES, duration, velocity))

                    with open('results.csv', 'a') as handle:
                        handle.write('"%s",%i,%i,%i,%.2f,%.2f\n' %
                                     (exchange_type, iteration, len(args.keys()),
                                      MESSAGES, duration, velocity))
                    print('Wrote results')

                    # Wait until all messages are consumed
                    while len(queue):
                        print 'Waiting for queue to drain'
                        time.sleep(5)

                    locals()['unbind_%s' % exchange_type](queue)

duration = time.time() - all_start
print('Benchmark complete in %s seconds' % duration)

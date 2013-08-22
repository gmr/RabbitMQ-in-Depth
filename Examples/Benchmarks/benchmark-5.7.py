import logging
import pika
import sys
import time
from pika.adapters import tornado_connection

LOGGER = logging.getLogger(__name__)

QOS = int(sys.argv[1]) if len(sys.argv) == 2 else None

ROUTING_KEY = 'benchmark_qos_%s' % QOS
PROPERTIES = pika.BasicProperties(content_type='text/plain', delivery_mode=1)

ITERATIONS = 100000

channel = None
consumer_tag = None
received = 0
start_time = None


with open('lorem.txt') as handle:
    BODY = handle.read()


def on_basic_cancel(_frame_unused):
        connection.close()



def on_message(channel, method_frame, header_unused, body_unused):
    global received

    channel.basic_ack(method_frame.delivery_tag)
    received += 1
    if received == ITERATIONS:
        total_time = time.time() - start_time
        velocity = float(ITERATIONS / total_time)
        LOGGER.info('Consumed %.2f messages/sec @ %s QoS in %.2f seconds',
                    velocity, 'unset' if QOS is None else QOS, total_time)
        channel.basic_cancel(on_basic_cancel, consumer_tag)


def on_basic_qosok(_frame_unsued):
    global consumer_tag, start_time
    LOGGER.info('Starting consumer')
    start_time = time.time()
    consumer_tag = channel.basic_consume(on_message, ROUTING_KEY)


def on_queue_declared(_frame_unused):
    LOGGER.info('Queue declared, publishing %i messages', ITERATIONS)
    for iteration in range(0, ITERATIONS):
        channel.basic_publish('', ROUTING_KEY, BODY[:2048], PROPERTIES)

    if QOS is not None:
        channel.basic_qos(callback=on_basic_qosok, prefetch_count=QOS)
    else:
        on_basic_qosok(None)


def on_channel_open(channel_opened):
    global channel

    LOGGER.info('Channel opened')
    channel = channel_opened
    channel.queue_declare(on_queue_declared, ROUTING_KEY,
                          auto_delete=True, durable=True, exclusive=True)


def on_open(connection):
    LOGGER.info('Connection opened')
    connection.channel(on_channel_open)


logging.basicConfig(level=logging.INFO)
LOGGER.info('Starting benchmark with QoS %s', QOS)
parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
connection = tornado_connection.TornadoConnection(parameters=parameters,
                                                  on_open_callback=on_open,
                                                  stop_ioloop_on_close=True)
try:
    connection.ioloop.start()
except KeyboardInterrupt:
    connection.close()
    connection.ioloop.start()

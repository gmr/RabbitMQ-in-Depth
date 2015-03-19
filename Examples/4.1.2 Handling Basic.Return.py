import datetime
import rabbitpy
import time

# Connect to the default URL of amqp://guest:guest@localhost:5672/%2F
with rabbitpy.Connection() as connection:
    with connection.channel() as channel:

        # Ensure the exchange still exists
        exchange = rabbitpy.Exchange(channel, 'chapter2-example')
        exchange.declare()

        body = 'server.cpu.utilization 25.5 1350884514'
        message = rabbitpy.Message(channel, body,
                                   {'content_type': 'text/plain',
                                    'timestamp': datetime.datetime.now(),
                                    'message_type': 'graphite metric'})

        message.publish('chapter2-example', 'server-metrics', mandatory=True)

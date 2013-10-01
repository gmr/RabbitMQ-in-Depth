import datetime
import rabbitpy

url = 'amqp://guest:guest@localhost:5672/%2f'
with rabbitpy.Connection(url) as connection:
    with connection.channel() as channel:
        exchange = rabbitpy.Exchange(channel, 'chapter4-example')
        exchange.declare()
        body = 'server.cpu.utilization 25.5 1350884514'
        message = rabbitpy.Message(channel,
                                   body,
                                   {'content_type': 'text/plain',
                                    'timestamp': datetime.datetime.now(),
                                    'message_type': 'graphite metric'})
        message.publish(exchange,
                        'server-metrics',
                        mandatory=True)

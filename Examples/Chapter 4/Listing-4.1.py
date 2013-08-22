import datetime
import rmqid

url = 'amqp://guest:guest@localhost:5672/%2f'             
with rmqid.Connection(url) as connection:                          #A
    with connection.channel() as channel:                          #B
        exchange = rmqid.Exchange(channel, 'chapter4-example')     #C
        exchange.declare()                                         #D
        body = 'server.cpu.utilization 25.5 1350884514'            #E
        message = rmqid.Message(channel,                           #F
                                body,                          
                                {'content_type': 'text/plain',
                                 'timestamp': datetime.datetime.now(),
                                 'message_type': 'graphite metric'})
        message.publish(exchange,                                  #G
                        'server-metrics',             
                        mandatory=True)

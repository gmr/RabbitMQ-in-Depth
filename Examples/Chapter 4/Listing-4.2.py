import datetime
import rmqid

connection = rmqid.Connection()                                    #A
try:
    with connection.channel() as channel:                          #B
        properties = {'content_type': 'text/plain',                #C
                      'timestamp': datetime.datetime.now(), 
                      'message_type': 'graphite metric'}
        body = 'server.cpu.utilization 25.5 1350884514'            #D
        message = rmqid.Message(channel, body, properties)         #E
        message.publish('chapter4-example',                        #F
                        'server-metrics',
                        mandatory=True)
except rmqid.exceptions.MessageReturnedException as error:         #G
    print('Message id %s returned: %s' % (error[0], error[2]))     #H

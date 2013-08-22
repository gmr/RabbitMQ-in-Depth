import rmqid

url = 'amqp://guest:guest@localhost:5672/%2f'
with rmqid.Connection(url) as connection:                          #A
    with connection.channel() as channel:                          #B
        channel.enable_publisher_confirms()                        #C
        message = rmqid.Message(channel,                           #D
                                'This is an important message',    
                                {'content_type': 'text/plain',
                                 'message_type': 'very important'})         

        if message.publish('chapter4-example',                     #E
                           'important.message'):         
            print('The message was confirmed')

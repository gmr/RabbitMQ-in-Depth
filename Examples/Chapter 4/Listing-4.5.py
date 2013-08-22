import rmqid

with rmqid.Connection() as connection:                           #A
    with connection.channel() as channel:                        #B
           
        tx = rmqid.Tx(channel)                                   #C
        tx.select()                                              #D

        message = rmqid.Message(channel,                         #E
                                'This is an important message',    
                                {'content_type': 'text/plain',
                                 'delivery_mode': 2,               
                                 'message_type': 'important'}) 
        message.publish('chapter4-example', 'important.message') #F
        try:
            if tx.commit():                                      #G        
                print('Transaction committed')             
        except rmqid.exceptions.NoActiveTransactionError:        #H
            print('Tried to commit without active transaction')

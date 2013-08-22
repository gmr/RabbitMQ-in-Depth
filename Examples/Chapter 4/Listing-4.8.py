import rmqid

connection = rmqid.Connection()                                    #A
with connection.channel() as channel:                              #B
    print('Channel is Blocked? %s' % channel.blocked())            #C

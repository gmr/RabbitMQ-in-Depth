import rabbitpy

with rabbitpy.Connection() as conn:
    with conn.channel() as channel:
        queue = rabbitpy.Queue(channel, 'test-messages')
        while True:
            message = queue.get()
            if message:
                message.pprint()
                message.ack()
                if message.body == 'stop':
                    break

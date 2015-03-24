import rabbitpy

message = rabbitpy.get(queue_name='mqtt-messages')
if message:
    message.pprint(True)
    message.ack()
else:
    print('No message in queue')

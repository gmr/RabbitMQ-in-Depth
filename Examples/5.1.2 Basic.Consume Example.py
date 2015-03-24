import rabbitpy

with rabbitpy.consume('amqp://guest:guest@localhost:5672/%2f',
                      'test-messages') as consume:
    for message in consume.next_message():
        message.pprint()
        message.ack()

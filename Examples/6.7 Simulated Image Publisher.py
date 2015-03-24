import datetime
import hashlib
import rabbitpy

with rabbitpy.Connection() as connection:
    with connection.channel() as channel:
        for iteration in range(100000):
            timestamp = datetime.datetime.now().isoformat()
            hash_value = hashlib.md5('%s:%s' % (timestamp, iteration))
            print
            msg = rabbitpy.Message(channel,
                                   'Image # %i' % iteration,
                                   {'headers':
                                     {'image-hash': str(hash_value.hexdigest())}},
                                    opinionated=True)
            msg.publish('image-storage')

import stomp
import pprint
import time

class Listener(stomp.ConnectionListener):

    can_stop = False
    def on_message(self, headers, message):
        if headers:
            print('\nHeaders:\n')
            pprint.pprint(headers)
        print('\nMessage Body:\n')
        print(message)
        self.can_stop = True

listener = Listener()

conn = stomp.Connection()
conn.set_listener('', listener)
conn.start()
conn.connect()

conn.subscribe('/queue/stomp-messages', id=1, ack='auto')

while not listener.can_stop:
	time.sleep(1)

conn.disconnect()

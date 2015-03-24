import stomp

conn = stomp.Connection()
conn.start()
conn.connect()
conn.send(body='Example Message',
          destination='/exchange/stomp-routing/example')
conn.disconnect()

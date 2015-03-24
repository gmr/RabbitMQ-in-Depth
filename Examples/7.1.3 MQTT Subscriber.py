import mosquitto
import os

client = mosquitto.Mosquitto('Subscriber-%s' % os.getpid())

def on_connect(mosq, obj, rc):
    if rc == 0:
        print('Connected')
    else:
        print('Connection Error')
client.on_connect = on_connect

def on_message(mosq, obj, msg):
    print('Topic: %s' % msg.topic)
    print('QoS: %s' % msg.qos)
    print('Retain: %s' % msg.retain)
    print('Payload: %s' % msg.payload)
    client.unsubscribe('mqtt/example')
client.on_message = on_message

def on_unsubscribe(mosq, obj, mid):
    print("Unsubscribe with mid %s received." % mid)
    client.disconnect()
client.on_unsubscribe = on_unsubscribe

client.connect("127.0.0.1")
client.subscribe("mqtt/example", 0)

while client.loop(timeout=1) == 0:
    pass

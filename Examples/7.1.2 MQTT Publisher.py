import mosquitto

client = mosquitto.Mosquitto('rmqid-test')
client.connect('localhost')
client.publish('mqtt/example', 'hello world from MQTT via Python', 1)
client.loop()
client.disconnect()
client.loop()

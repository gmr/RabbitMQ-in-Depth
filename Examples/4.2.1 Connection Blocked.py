import rabbitpy

connection = rabbitpy.Connection()
print('Channel is Blocked? %s' % connection.blocked)

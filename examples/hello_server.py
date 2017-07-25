import time
from pyserve import Server

class HelloHandler:
    def __init__(self, message='Hello World!', wait_before_message=2):
        self.wait_before_message = wait_before_message
        self.message = message
        self.data = {}

    def __call__(self, server, connection_id):
        connection = server.get_connection(connection_id)
        if connection_id not in self.data:
            self.data[connection_id] = {
                'created': time.time()
            }
        current_time = time.time()
        create_time = self.data[connection_id]['created']
        if current_time - create_time >= self.wait_before_message:
            connection.send(self.message)
            server.remove_connection(connection_id)

HOSTNAME = '127.0.0.1'
PORT = 5050

hello_handler = HelloHandler(message='Hello!!!', wait_before_message=5)
server = Server(HOSTNAME, PORT, verbose=True)
server.run(hello_handler)

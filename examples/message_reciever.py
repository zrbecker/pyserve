from pyserve import Server

def message_handler(server, connection_id):
    connection = server.get_connection(connection_id)
    try:
        message = connection.recv(512)
        print(message.decode('utf-8'))
        connection.send('Thank You!')
        server.remove_connection(connection_id)
    except BlockingIOError:
        pass

server = Server('127.0.0.1', 5050, verbose=True)
server.run(message_handler)
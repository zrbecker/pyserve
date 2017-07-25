import socket
import sys

class Connection:
    def __init__(self, sock, address):
        self.sock = sock
        self.address = address

    def send(self, message, encoding='utf-8'):
        self.sock.send(message.encode(encoding))

    def close(self):
        self.sock.close()

class Server:
    def __init__(self, hostname, port, max_queue=10, max_connections=10,
            verbose=False):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.sock.setblocking(False)
        self.sock.bind((hostname, port))
        self.sock.listen(max_queue)

        self.connections = {}
        self.max_connections = max_connections
        self.next_connection_id = 0

        self.verbose = verbose

    def accept_new_connections(self, limit=10):
        connection = None
        try:
            connection = Connection(*self.sock.accept())
        except BlockingIOError:
            return  # No more connections
        if connection:
            self.add_connection(connection)

    def add_connection(self, conn):
        if self.verbose:
            print('client connected {}:{}'.format(*conn.address))
        id = self.next_connection_id
        self.next_connection_id += 1
        self.connections[id] = conn
        return id

    def remove_connection(self, conn_id):
        conn = self.connections.pop(conn_id, None)
        if self.verbose:
            print('client disconnected {}:{}'.format(*conn.address))
        if conn:
            conn.close()

    def get_connection(self, conn_id):
        return self.connections.get(conn_id)

    def run_once(self, connection_handler):
        self.accept_new_connections()
        for conn_id in list(self.connections.keys()):
            connection_handler(self, conn_id)

    def run(self, connection_handler):
        if self.verbose:
            print('Server Listening {}:{}'.format(*self.sock.getsockname()))
        try:
            error_count = 0
            while True:
                try:
                    self.run_once(connection_handler)
                except socket.herror as e:
                    print('socket.herror:', e, file=sys.stderr)
                    error_count += 1
                except socket.gaierror as e:
                    print('socket.gaierror:', e, file=sys.stderr)
                    error_count += 1
                except socket.timeout as e:
                    print('socket.timeout:', e, file=sys.stderr)
                    error_count += 1
                except OSError as e:
                    print('OSError:', e, file=sys.stderr)
                    error_count += 1
                if error_count >= 10:
                    break
        except KeyboardInterrupt:
            print('KeyboardInterrupt ending program.')
            return

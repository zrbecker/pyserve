import socket

class Client:
    def __init__(self, hostname, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((hostname, port))

    def send(self, message, encoding='utf-8'):
        self.sock.send(message.encode(encoding))

    def recv(self, bufsize):
        return self.sock.recv(bufsize)

    def close(self):
        self.sock.close()

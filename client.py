import socket

IP = '127.0.0.1'
PORT = 5000

# TODO: encrypt server-client comms via ssl


class Client:
    def __init__(self):
        self.sock = socket.socket()
        try:
            self.sock.connect((IP, PORT))
        except Exception as e:
            print(e)
            self.sock = None
            # encrypt key and store locally, wait for server

    def send(self, msg):
        if self.sock is not None:
            self.sock.send(msg)

    def recv(self):
        return self.sock.recv(1024)

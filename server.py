import socket
import threading
import json

IP = '127.0.0.1'
PORT = 5000

# TODO: encrypt server-client comms via ssl


class ThreadedServer(object):
    def __init__(self):
        self.host = IP
        self.port = PORT
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target=self.listenToClient, args=(client, address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    with open('entry.txt', 'a') as fd:
                        json.dump(json.loads(data), fd)
                        fd.write('\n')
                    response = "OK"
                    client.send(response.encode('utf-8'))
                else:
                    raise BlockingIOError('Client disconnected')
            except:
                client.close()
                return False


if __name__ == "__main__":
    server = ThreadedServer()
    server.listen()

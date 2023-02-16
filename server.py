import socket
import time

class Server:
    def __init__(self):
        self.serv = socket.socket()
        self.serv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.serv.bind(('', 80))
        self.serv.listen(1)

        while True:
            self.conn, self.addr = self.serv.accept()

            request = self.conn.recv(1024)
            route = request.decode('utf-8').split(" ")[1]
            if (route == '/'):
                self.establishConnection()
                break

    def establishConnection(self):
        #response = '<html><body><h1>Siema</h1></body></html>'
        self.conn.send('HTTP/1.1 200 OK\n')
        self.conn.send('Content-type: application/json\n')
        self.conn.send('Connection: close\n\n')
        self.conn.sendall('{status: 1, message: "connected"}')
        self.conn.close()
    def send(self, message):
        self.conn.sendall(message)
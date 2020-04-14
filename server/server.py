#!/usr/bin/python

import socket, threading
from sense_hat import SenseHat

class ServerThread(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.clients = {}

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', self.port))

        print "Server started on port {}, waiting for clients to connect...".format(self.port)
        while True:
            server.listen(1)
            clientSocket, clientAddress = server.accept()

            print "Incoming connection from {}".format(clientAddress)
            client = ClientThread(clientAddress, clientSocket)
            client.setDaemon(True)
            client.start()
            self.addClient(clientAddress, client)
            print "Client {} added to the list".format(clientAddress)


    def addClient(self, clientAddress, client):
        self.removeClient(clientAddress)
        self.clients[clientAddress] = client

    def removeClient(self, clientAddress):
        if clientAddress in self.clients:
            self.clients.pop(clientAddress)
            print "Client {} removed from the list".format(clientAddress)

    def sendMessage(self, message):
        for clientAddress, client in self.clients.items():
            client.sendMessage(message)


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientSocket):
        threading.Thread.__init__(self)
        self.socket = clientSocket
        self.clientAddress = clientAddress

    def run(self):
        try:
            while True:
                data = self.socket.recv(2048)
                if not data:
                    break
                # Do we need to do anything with incoming messages ?
                # message = data.decode()
                # print "Received message ", message, " from client ", self.clientAddress
        except socket.error as e:
            print "Closed connection from {}".format(self.clientAddress)
        finally:
            server.removeClient(self.clientAddress)

    def sendMessage(self, message):
        print "Sending message {} to {}".format(message, self.clientAddress)
        message = message + "\n"
        self.socket.send(message.encode())



server = ServerThread(80)
server.setDaemon(True)
server.start()

sense = SenseHat()

running = True

while running:
  for event in sense.stick.get_events():
    if event.action in ("pressed", "held"):
      if event.direction == "right":
          print ("Key RIGHT pressed on SenseHat")
          server.sendMessage("RIGHT")

      elif event.direction == "left":
          print ("Key LEFT pressed on SenseHat")
          server.sendMessage("LEFT")

      elif event.direction == "up":
          print ("Key UP pressed on SenseHat")
          server.sendMessage("UP")

      elif event.direction == "down":
          print ("Key DOWN pressed on SenseHat")
          server.sendMessage("DOWN")

      elif event.direction == "middle":
          print ("Key MIDDLE pressed on SenseHat")
          print ("Stopping program")
          running = False

global onCommandReceived
global onBrowserClosed
global browserclients
import struct
import os
from twisted.internet.protocol import ServerFactory, Protocol
browserclients = []
onCommandReceived = []
onBrowserClosed = []

class ClientConnection(Protocol):
    magic = 987654321
    data = ''
    headerformat = '!III'
    headersize = struct.calcsize(headerformat)
    datasize = 0
    cmd = 0

    def dataReceived(self, data):
        self.data += data
        while len(self.data):
            if self.datasize == 0 and len(self.data) >= self.headersize:
                magic, self.cmd, self.datasize = struct.unpack(self.headerformat, self.data[:self.headersize])
                self.data = self.data[self.headersize:]
                if magic != self.magic:
                    self.data = ''
                    self.datasize = 0
            if len(self.data) >= self.datasize:
                for x in onCommandReceived:
                    x(self.cmd, self.data[:self.datasize])
                    break
                self.data = self.data[self.datasize:]
                self.datasize = 0
            else:
                break

    def connectionMade(self):
        browserclients.append(self)

    def connectionLost(self, reason):
        browserclients.remove(self)
        if not len(browserclients):
            for x in onBrowserClosed:
                x()

class CommandServer:

    def __init__(self):
        from twisted.internet import reactor
        self.factory = ServerFactory()
        self.factory.protocol = ClientConnection
        try:
            os.remove('/tmp/.sock.netflix')
        except:
            pass
        else:
            pass
        self.port = reactor.listenUNIX('/tmp/.sock.netflix', self.factory)

    def __del__(self):
        for client in browserclients:
            client.transport.loseConnection()

    def sendCommand(self, cmd, data=''):
        for client in browserclients:
            client.transport.write(struct.pack('!III', client.magic, cmd, len(data)))
            if len(data):
                client.transport.write(data)

    def connectedClients(self):
        return len(browserclients)

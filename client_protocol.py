


from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ClientFactory


import struct

from twisted.internet.protocol import Protocol, ClientFactory
from twisted.protocols.basic import IntNStringReceiver


class ClientProtocol(LineReceiver):
    
    def lineReceived(self, msg):
        self.factory.receiveMessage(msg)

    def connectionMade(self):
        self.factory.clientReady(self)

    def connectionLost(self, reason):
        self.factory.receiveMessage("Connection lost.")

class ClientProtocolFactory(ClientFactory):
    protocol = ClientProtocol

    def __init__(self, handleReceivedMessage):
        self.handleReceivedMessage = handleReceivedMessage
    
    def clientReady(self, client):
        self.receiveMessage("Connected.")
        self.client = client

    def receiveMessage(self, msg):
        self.handleReceivedMessage("CHAT", msg)

    def sendMessage(self, msg):
        if self.client:
            self.client.sendLine(msg)
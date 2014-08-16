
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory


class ServerProtocol(LineReceiver):
    def __init__(self, factory, handleReceivedMessage):
        self.factory = factory
        self.name = None
        self.state = "REGISTER"
        self.handleReceivedMessage = handleReceivedMessage
        
    def connectionMade(self):
        self.sendLine("What's your name?")

    def connectionLost(self, reason):
        if self.name in self.factory.users:
            del self.factory.users[self.name]
            self.handleReceivedMessage("REMOVEUSER", self.name)
            self.broadcastMessage("%s has left the channel." % (self.name,))

    def lineReceived(self, line):
        if self.state == "REGISTER":
            self.handleRegistration(line)
        else:
            self.handleChat(line)

    def broadcastMessage(self, message):
        for name, protocol in self.factory.users.iteritems():
            protocol.sendLine(message)

    def handleRegistration(self, name):
        if name in self.factory.users:
            self.sendLine("Name already in user, please choose another.")
        else:
            self.sendLine("> Welcome, %s!" % (name,))
            self.broadcastMessage("%s has joined the channel." % (name,))
            self.factory.users[name] = self
            self.handleReceivedMessage("ADDUSER", name)
            self.state = "CHATTING"
            self.name = name

    def handleChat(self, message):
        message = "<%s> %s" % (self.name, message)
        self.broadcastMessage(message)
        self.handleReceivedMessage("TOCHAT", message)

class ServerProtocolFactory(Factory):
    def __init__(self, handleReceivedMessage):
        self.users = {}
        self.handleReceivedMessage = handleReceivedMessage
        
    def buildProtocol(self, addr):
        return ServerProtocol(self, self.handleReceivedMessage)
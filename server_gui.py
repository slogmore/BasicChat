import sys

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic
import qt4reactor

from server_protocol import ServerProtocolFactory

class ServerWindow(QtGui.QMainWindow):

    def __init__(self, reactor):
        self.initializeUI()
        self.initializeReactor(reactor)
            
    def initializeUI(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi('GUI\serverui.ui', self)
        self.userCount = 0
        self.ui.show()
        
    def initializeReactor(self, reactor):
        self.reactor = reactor
        self.factory = ServerProtocolFactory(self.handleReceivedMessage)
        self.connection = self.reactor.listenTCP(10000, self.factory)

    def handleReceivedMessage(self, cmd, msg):
        if cmd == "TOCHAT": 
            self.toChat(msg)
        elif cmd == "ADDUSER": 
            self.addUser(msg)
        elif cmd == "REMOVEUSER": 
            self.removeUser(msg)

    def toChat(self, msg):
        self.ui.txtEditChat.append(msg)
  
    def addUser(self, username):
        self.userCount += 1
        self.ui.lblUserCount.setText("User count: " + str(self.userCount))
        self.ui.listUsers.addItem(username)

    def removeUser(self, username):
        self.userCount -= 1
        self.ui.lblUserCount.setText("User count: " + str(self.userCount))
        self.toChat("User " + username +" leaving")
        for index in xrange(self.ui.listUsers.count()): 
            currentItem = self.ui.listUsers.item(index)
            itemStr = currentItem.text()
            if(itemStr == username):
                self.ui.listUsers.takeItem(index)

    def closeEvent(self, event):
        self.connection.disconnect()
        self.reactor.stop()
        event.accept()

def main():
    app = QtGui.QApplication(sys.argv)
    qt4reactor.install()
    from twisted.internet import reactor
    serverWindow = ServerWindow(reactor)
    reactor.run()

if __name__ == '__main__':
    main()


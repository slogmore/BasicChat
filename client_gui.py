import sys
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic
import qt4reactor

from client_protocol import ClientProtocolFactory

class ClientWindow(QtGui.QMainWindow):

    def __init__(self, reactor):
        self.reactor = reactor
        self.initializeUI()
        self.initializeReactor(reactor)

    def initializeUI(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi('GUI\clientui.ui', self)
        self.ui.show()
        self.ui.lineEditCmdLine.returnPressed.connect(self.handleCmdLine)
        self.ui.lineEditCmdLine.setFocus()

    def initializeReactor(self, reactor):
        self.reactor = reactor
        self.factory = ClientProtocolFactory(self.handleReceivedMessage)
        self.connection = self.reactor.connectTCP("127.0.0.1", 10000, self.factory)

    def handleReceivedMessage(self, cmd, msg):
        if(cmd == "CHAT"):
            self.addToChat(msg)

    def handleSendMessage(self, msg):
        self.factory.sendMessage(msg)

    def handleCmdLine(self):
        msg = str(self.ui.lineEditCmdLine.text())
        self.handleSendMessage(msg)
        self.ui.lineEditCmdLine.clear()

    def addToChat(self, msg):
        self.ui.txtMain.append(str(msg))

    def connectFail(self, reason):
        self.addToChat("Disconnected")
        self.connection.diconnect()

    def closeEvent(self, event):
        self.connection.disconnect()
        self.reactor.stop()
        event.accept()


def main():
    app = QtGui.QApplication(sys.argv)
    qt4reactor.install()
    from twisted.internet import reactor
    clientWindow = ClientWindow(reactor)
    reactor.run()

if __name__ == '__main__':
    main()


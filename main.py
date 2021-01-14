from PyQt5 import QtWidgets
from Name_window import Ui_MainWindow
import sys
import socket
import threading
import json
from Chat import Ui_MainWindow_Chat
class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.HEADER = 64
        self.PORT = 5050
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = "172.20.10.2"
        self.ADDR = (self.SERVER ,self.PORT)
        self.ui.pushButton.clicked.connect(self.Chat)
        self.ui.ui.pushButton.clicked.connect(self.GetEnteredText)
        
    def Chat(self):
        self.myname=self.ui.textEdit.toPlainText()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        self.client.send(self.myname.encode(self.FORMAT))

        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()
        self.ui.window2.show()
    def send(self, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        

    def receive(self):
        while True:
            
            data = self.client.recv(2048).decode(self.FORMAT)
            data_loaded = json.loads(data)
            if data_loaded["identitiy"] == "Me":
                self.InserText("Me : " + data_loaded["message"] , "Me")
                
            else:
                self.InserText(data_loaded["identitiy"] + " : "+ data_loaded["message"], "Not Me")
                

    def InserText(self, msg, identitiy):
        
        if identitiy == "Me":
            word = '<p  style=\" color: #008000; font-size: 16pt;  \">%s</p>' % msg
        elif identitiy == "Not Me":
            word = '<p  style=\" color: #00008B; font-size: 16pt;  \">%s</p>' % msg
            
        self.ui.ui.textBrowser.append(word)

    def GetEnteredText(self):
        textBoxValue = self.ui.ui.textEdit.toPlainText()
        self.send(textBoxValue)
        self.ui.ui.textEdit.clear() 

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()
    application.send("!DISCONNECT")

if __name__ == "__main__":
    main()

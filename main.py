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
        self.PORT = 55555
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = '127.0.0.1'
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
        #print(self.myname)

    def receive(self):
        while True:
            # try:
            data = self.client.recv(2048).decode(self.FORMAT)
            data_loaded = json.loads(data)
            if data_loaded["identitiy"] == "Me":
                self.InserText("Me : " + data_loaded["message"] , "Me")
                # print("Me : " + data_loaded["message"])
            else:
                self.InserText(data_loaded["identitiy"] + " : "+ data_loaded["message"], "Not Me")
                # print("some one : " + data_loaded["message"]) 

    def InserText(self, msg, identitiy):
        # msg ="Helllo"
        # for i in range(50):
        if identitiy == "Me":
            word = '<p  style=\" color: #000000; font-size: 16pt;  \">%s</p>' % msg
        elif identitiy == "Not Me":
            word = '<p  style=\" color: #00008B; font-size: 16pt;  \">%s</p>' % msg
            # word = '<span  style=\" color: #ff0000; font-size: 20px;  \">%s</span>' % mesg
        self.ui.ui.textBrowser.append(word)

    def GetEnteredText(self):
        textBoxValue = self.ui.ui.textEdit.toPlainText()
        # print(textBoxValue)
        # self.InserText(textBoxValue)
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

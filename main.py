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
        self.ui = Ui_MainWindow() #GUI of the enter username window
        self.ui.setupUi(self)
        self.HEADER = 64
        self.PORT = 55555
        self.FORMAT = 'utf-8' # decoding format
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = socket.gethostbyname(socket.gethostname()) # IPv4 address of the server
        self.ADDR = (self.SERVER ,self.PORT) # Ipv4 and port number
        self.ui.pushButton.clicked.connect(self.Chat) # when clicked sumbits the user name to the server and opens the chatting window
        self.ui.ui.pushButton.clicked.connect(self.GetEnteredText) # when clicked gets the text of the texting field
        
    def Chat(self):
        self.myname=self.ui.textEdit.toPlainText() # get the entered name
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # setting the client socket
        self.client.connect(self.ADDR) # connecting to the socket server
        self.client.send(self.myname.encode(self.FORMAT)) # sending the entered user name to the server

        self.receive_thread = threading.Thread(target=self.receive) # creating a thread for the receive function
        self.receive_thread.start() # starting the thread
        self.ui.window2.show() # showing the chatting window

    def send(self, msg):
        message = msg.encode(self.FORMAT) # encoding the message before sending
        msg_length = len(message) # get message lenght to be sent first
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length)) # sending the lenght of the message in 64 bytes 
        self.client.send(send_length) # sending lenght to the server
        self.client.send(message) # then sending the message itself
        #print(self.myname)

    def receive(self):
        while True:
            
            data = self.client.recv(2048).decode(self.FORMAT) # received messages from the server
            data_loaded = json.loads(data) # converting it back to dictionary
            if data_loaded["identitiy"] == "Me": # if it was the message I sent , pass it to the isertText function with "Me"  
                self.InserText("Me : " + data_loaded["message"] , "Me")
                
            else:
                self.InserText(data_loaded["identitiy"] + " : "+ data_loaded["message"], "Not Me") # if the message from some one else , pass it to the isertText function with "Not Me"
                

    def InserText(self, msg, identitiy): # to display the messages 
        
        if identitiy == "Me":
            word = '<p  style=\" color: #000000; font-size: 16pt;  \">%s</p>' % msg # if me display with color black
        elif identitiy == "Not Me":
            word = '<p  style=\" color: #00008B; font-size: 16pt;  \">%s</p>' % msg  # if me display with color blue
            # word = '<span  style=\" color: #ff0000; font-size: 20px;  \">%s</span>' % mesg
        self.ui.ui.textBrowser.append(word) # display the message

    def GetEnteredText(self):
        textBoxValue = self.ui.ui.textEdit.toPlainText() # get the entered message
        
        try:
            self.send(textBoxValue) # send it to the socker server
            self.ui.ui.textEdit.clear() # then clear the text area

        except ConnectionAbortedError:  # if client disconneted from the server because of timeout
            self.ui.ui.textEdit.clear() # clear the text area
            self.ui.ui.textBrowser.append('you are disconnected') # display client disconnected



def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()
    application.send("!DISCONNECT") # disconnect the client if the GUI is closed

if __name__ == "__main__":
    main()

import socket
import threading
import json
HEADER = 64  #header is 64 bytes
PORT = 55555 #port number
from cryptography.fernet import Fernet # encryption library
SERVER = socket.gethostbyname(socket.gethostname()) #local IPv4 address
ADDR = (SERVER ,PORT) # IPv4 and port number
FORMAT = 'utf-8'  # encoding format for messages
DISCONNECT_MESSAGE = "!DISCONNECT" # if sent by the client it will be disconnected from the server
key = b'M30gFM5sbouc49LUU-qkxCQncI_2aQcpSwepfvEwlPU=' #encryption key

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # starting the server with TCP
server.bind(ADDR)

Clients = [] #list to save iddress of conected clients
Clients_Names = [] #list to save user name of conected clients


# Sending Messages To All Connected Clients
def broadcast(message , sending_client):
    for client in Clients: # Sending Messages To All Connected Clients
        cipher_suite = Fernet(key) #suite the Fernet key
        if client == sending_client: #if the client is the sender
            #incoding msg in jason format
            data = {"message": message , "identitiy": "Me" }
            print(f'sending_client = {sending_client}')
        else: #if the client is not  the sender
            index =Clients.index(sending_client) #getting index of the conn in array
            data = {"message": message , "identitiy": Clients_Names[index] }#incoding msg in jason format
        data_string = json.dumps(data) #serializing meassage in to string
        print("data" , data_string)
        client.send(cipher_suite.encrypt(data_string.encode(FORMAT))) #encryt and sending message to clients
        


def handle_client(conn, addr):
    index = Clients.index(conn)
    print(f"[NEW CONNECTION]  {addr} ( {Clients_Names[index]} ) has connected.")
    connected = True
    try:
        while connected:
            conn.settimeout(100) #setting timeout after 100 second (it will raise time out Exception if client was idle)
            msg_lenght = conn.recv(HEADER).decode(FORMAT) #recieve msg lenth
            conn.settimeout(None) # cancleing timeout timer as the client sent message header
            if msg_lenght:
                # try:
                msg_lenght = int(msg_lenght) 
                print(msg_lenght)
                msg = conn.recv(msg_lenght) #recieve msg with the size sent before
                cipher_suite = Fernet(key) #suite a fernet key
                msg = cipher_suite.decrypt(msg) #decrypting msg
                msg=msg.decode(FORMAT) # converting msg to string
                broadcast(msg, conn) # function to form the data in dictionary to handle identity of users
                if msg == DISCONNECT_MESSAGE: #if client closes the ui
                    connected = False
                    #removing client data from clients and names lists
                    index = Clients.index(conn) #getting index of the conn in array
                    Clients.remove(conn) #remove client address
                    Clients_Names.remove(Clients_Names[index]) #remove client name
                    print(f"[{addr}] left!")
                print(f"[{addr}] {msg}")
    except Exception: #occurs when client is idle
        connected = False
        index = Clients.index(conn) #getting index of the conn in array
        #removing client data from clients and names lists
        Clients.remove(conn) #remove client address
        Clients_Names.remove(Clients_Names[index]) #remove client name
        print(f"[{addr}] was disconnected (Idle client)")
        
    conn.close() #closing connection 



def start():
    server.listen() # listen for new connections
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn , adrr = server.accept() #accepting slient request for connect
        Clients.append(conn) # appending new conn in array
        name=conn.recv(4096) #recieving user name
        cipher_suite = Fernet(key) #suite the key
        name = cipher_suite.decrypt(name).decode(FORMAT) #decrypting name
        Clients_Names.append(name) # appending new conn user name in array
        thread = threading.Thread(target=handle_client, args=(conn, adrr)) #initializing thread for every client
        thread.start() #starting thread
        print(f"[ACTIVE CONNECTIONS]  : {threading.activeCount() - 1}") #number of threads = number of clients


print("[STARTING] server is starting...")
start() #call start to initialize server
    

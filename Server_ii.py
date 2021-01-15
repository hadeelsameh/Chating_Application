import socket
import threading
import json
HEADER = 64  #header is 64 bytes
PORT = 55555

SERVER = socket.gethostbyname(socket.gethostname()) #local IPv4 address
ADDR = (SERVER ,PORT) # IPv4 and port number
FORMAT = 'utf-8'  # encoding format for messages
DISCONNECT_MESSAGE = "!DISCONNECT" # if sent by the client it will be disconnected from the server

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # starting the server with TCP
server.bind(ADDR)

Clients = [] #list to save iddress of conected clients
Clients_Names = [] #list to save user name of conected clients


# Sending Messages To All Connected Clients
def broadcast(message , sending_client):
    for client in Clients:
        if client == sending_client:
            #incoding msg in jason format
            data = {"message": message , "identitiy": "Me" }
            print(f'sending_client = {sending_client}')
        else: 
            index =Clients.index(sending_client) #getting index of the conn in array
            data = {"message": message , "identitiy": Clients_Names[index] }
        data_string = json.dumps(data) #serializing meassage in to string
        print("data" , data_string)
        client.send(data_string.encode(FORMAT)) #sending message to clients
        


def handle_client(conn, addr):
    index = Clients.index(conn)
    print(f"[NEW CONNECTION]  {addr} ( {Clients_Names[index]} ) had connected.")
    connected = True
    try:
        while connected:
            conn.settimeout(100) #setting timeout after 100 second (it will raise time out Exception if client was idle)
            msg_lenght = conn.recv(HEADER).decode(FORMAT) 
            conn.settimeout(None) # cancleing timeout timer as the client sent message header
            if msg_lenght:
                # try:
                msg_lenght = int(msg_lenght)
                msg = conn.recv(msg_lenght).decode(FORMAT)
                broadcast(msg, conn)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    #removing client data from clients and names lists
                    index = Clients.index(conn) #getting index of the conn in array
                    Clients.remove(conn)
                    Clients_Names.remove(Clients_Names[index])
                    print(f"[{addr}] left!")
                print(f"[{addr}] {msg}")
    except Exception: #occurs when client is idle
        connected = False
        index = Clients.index(conn)
        #removing client data from clients and names lists
        Clients.remove(conn) 
        Clients_Names.remove(Clients_Names[index])
        print(f"[{addr}] was disconnected (Idle client)")
        
    conn.close() #closing connection 



def start():
    server.listen() # listen for new connections
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn , adrr = server.accept()
        Clients.append(conn) # appending new conn in array
        Clients_Names.append(conn.recv(HEADER).decode(FORMAT)) # appending new conn user name in array
        #print(Clients_Names)
        thread = threading.Thread(target=handle_client, args=(conn, adrr)) #initializing thread for every client
        thread.start() #starting thread
        print(f"[ACTIVE CONNECTIONS]  : {threading.activeCount() - 1}") #number of threads = number of clients


print("[STARTING] server is starting...")
start()
    

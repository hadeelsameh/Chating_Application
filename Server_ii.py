import socket
import threading
import json
HEADER = 64  #header is 64 bytes
PORT = 55555

SERVER = '127.0.0.1' #local IPv4 address
ADDR = (SERVER ,PORT) # IPv4 and port number
FORMAT = 'utf-8'  # encoding format for messages
DISCONNECT_MESSAGE = "!DISCONNECT" # if sent by the client it will be disconnected from the server

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # starting the server with TCP
server.bind(ADDR)

Clients = []
Clients_Names = []


# Sending Messages To All Connected Clients
def broadcast(message , sending_client):
    for client in Clients:
        if client == sending_client:
            data = {"message": message , "identitiy": "Me" }
            print(f'sending_client = {sending_client}')
        else: 
            index =Clients.index(sending_client)
            data = {"message": message , "identitiy": Clients_Names[index] }
        data_string = json.dumps(data)
        print("data" , data_string)
        client.send(data_string.encode(FORMAT))
        # client.send(message)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_lenght = conn.recv(HEADER).decode(FORMAT)
        if msg_lenght:
            # try:
            msg_lenght = int(msg_lenght)
            msg = conn.recv(msg_lenght).decode(FORMAT)
            # msg = conn.recv(msg_lenght)
            broadcast(msg, conn)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                index = Clients.index(conn)
                Clients.remove(conn)
                Clients_Names.remove(Clients_Names[index])
                print(f"[{addr}] left!")
            print(f"[{addr}] {msg}")

                # conn.send("Msg received".encode(FORMAT))
            # except:
            #     # Removing And Closing Clients
            #     # index = Clients.index(conn)
            #     Clients.remove(conn)
            #     conn.close()
            #     print(f"[{addr}] left!")
            #     # nickname = nicknames[index]
            #     # broadcast('{} left!'.format(nickname).encode('ascii'))
            #     # nicknames.remove(nickname)
            #     break
    conn.close()



def start():
    server.listen() # listen for new connections
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn , adrr = server.accept()
        Clients.append(conn)
        Clients_Names.append(conn.recv(HEADER).decode(FORMAT))
        print(Clients_Names)
        thread = threading.Thread(target=handle_client, args=(conn, adrr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()
    

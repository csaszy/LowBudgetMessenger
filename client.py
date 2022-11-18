import socket
import threading

HEADER = 64 
PORT = 5050  #88 , 80
DISCONNENCT_MSG = "!DISCONNECT"
SERVER = "192.168.1.72"
FORMAT = "utf-8"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def Recv():
    connected = True
    while connected:
        msg_length = client.recv(HEADER).decode(FORMAT) #blocking code --> block the flow until it receves a message
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
            if msg == DISCONNENCT_MSG:
                connected = False
            print(f'- {msg}')
    client.close()

def Send():
    while True:
        message = input("").encode(FORMAT)
        msg_length = len(message)
        if msg_length:
            send_length = str(msg_length).encode(FORMAT)
            send_length += b" " * (HEADER-len(send_length)) #make it 64 bytes
            client.send(send_length)
            client.send(message)
            if message == DISCONNENCT_MSG:
                print("--------------------|You disconnected from the server|--------------------")

sendThread = threading.Thread(target=Send)
recvThread = threading.Thread(target=Recv)

if __name__ == "__main__":
    sendThread.start()
    recvThread.start()
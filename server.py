import socket
import threading

HEADER = 64 
PORT = 5050  #88 , 80
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNENCT_MSG = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

class Client:
    def __init__(self, id, conn, addr) -> None:
        #print('obj created')
        self.conn = conn
        self.addr = addr
        self.id = id
        self.connected = True
        #self.thread = threading.Thread(target=self.Recv) 
        #self.thread.start()
    def Send(self, msg, send_length):
       #msg_length = len(msg)
       #send_length = str(msg_length).encode(FORMAT)
       #send_length += b" " * (HEADER-len(send_length)) #make it 64 bytes
        self.conn.sendto(send_length,(self.addr[0],self.addr[1]))
        self.conn.sendto(msg,(self.addr[0],self.addr[1]))
    def Recv(self):
        #print(f'{self.id} receiving')
        msg_length = self.conn.recv(HEADER) #blocking code --> block the flow until it receves a message
        if msg_length:
            msg = self.conn.recv(int(msg_length))#.decode(FORMAT)
            if msg == DISCONNENCT_MSG:
                self.connected = False
        return msg, msg_length
    def Get(self):
        return self.id,self.conn,self.addr

clients = []

def handleClient(client: Client): #conn = connection; addr = address
    id, conn, addr = client.Get()
    print(f"[NEW_CONNECTION] --> {addr} connected")
    while True:
        rawMsg, length = client.Recv()
        print(f"[{client.Get()[-1]}]: {rawMsg.decode(FORMAT)}")
        for c in clients:
            if c != client:
                c.Send(rawMsg,length)
    #connected = True
    #while connected:
    #    msg_length = conn.recv(HEADER).decode(FORMAT) #blocking code --> block the flow until it receves a message
    #    if msg_length:
    #        msg_length = int(msg_length)
    #        msg = conn.recv(msg_length).decode(FORMAT)
    #        if msg == DISCONNENCT_MSG:
    #            connected = False
    #        print(f"[{addr}]: {msg}")
    #        for i in clients:
    #            if addr != i[1]:
    #                msg_length = len(msg)
    #                send_length = str(msg_length).encode(FORMAT)
    #                send_length += b" " * (HEADER-len(send_length)) #make it 64 bytes
    #                i[0].sendto(send_length,(i[1][0], i[1][1]))
    #                i[0].sendto(msg.encode(FORMAT),(i[1][0], i[1][1]))
    #conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Listening on {SERVER}")
    while True:
        conn, addr = server.accept() #awaits for a new connection

        client = Client(threading.active_count()-1,conn,addr)
        clients.append(client)

        thread = threading.Thread(target=handleClient, args=(client,))
        thread.start()
        print(f"[ACTIVE_CONNECTION] --> {threading.active_count()-1}")

if __name__ == "__main__":
    print("[STARTING]...")
    start()
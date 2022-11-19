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
        self.conn = conn
        self.addr = addr
        self.id = id
        self.connected = True
    def Send(self, msg, send_length):
        self.conn.sendto(send_length,(self.addr[0],self.addr[1]))
        self.conn.sendto(msg,(self.addr[0],self.addr[1]))
    def Recv(self):
        #print(f'{self.id} receiving')
        try:
            msg_length = self.conn.recv(HEADER) #blocking code --> block the flow until it receves a message
        except:
            return DISCONNENCT_MSG, 0
        if msg_length:
            msg = self.conn.recv(int(msg_length))
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
        msg, length = client.Recv()
        if msg == DISCONNENCT_MSG: #detect disconnected clients
            clients.remove(client)
            print(f"[{client.Get()[-1]}]: Disconnected")
            print(f"[ACTIVE_CONNECTION] --> {len(clients)}")
            while True: pass  #freezing the thread
        print(f"[{client.Get()[-1]}]: {msg.decode(FORMAT)}")
        for c in clients:
            if c != client:
                c.Send(msg,length)

def start():
    server.listen()
    print(f"[LISTENING] Listening on {SERVER}")
    while True:
        conn, addr = server.accept() #awaits for a new connection

        client = Client(threading.active_count()-1,conn,addr)
        clients.append(client)

        thread = threading.Thread(target=handleClient, args=(client,))
        thread.start()
        print(f"[ACTIVE_CONNECTION] --> {len(clients)}")

if __name__ == "__main__":
    print("[STARTING]...")
    start()
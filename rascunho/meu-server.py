import socket
import threading

HEADER = 2048
PORT = 12000
SERVER = ""
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "sair"
SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)



def get(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        return conn.recv(msg_length).decode(FORMAT)
    else:
        return DISCONNECT_MESSAGE

def send(conn, msg):
    try:
        conn.send(msg.encode(FORMAT))
    except:
        print("Não existe mais conexão!")
        return


def handle_client(conn, addr):
    print(f"[NOVA CONEXÃO] {addr} conectado.")

    connected = True
    
    while connected:
        msg = get(conn)
        print(f"[{addr} {msg}]")
        
        if msg.lower() == "enviar arquivo":
            send(conn, "Nome do arquivo: ")
            msg = get(conn)
            
           
            filename = conn.recv(SIZE).decode(FORMAT)
            print(f"[RECV] Receiving the filename.")
            file = open(filename, "w")
            conn.send("Filename received.".encode(FORMAT))

            data = conn.recv(SIZE).decode(FORMAT)
            print(f"[RECV] Receiving the file data.")
            file.write(data)
            conn.send("File data received".encode(FORMAT))
            file.close()

       

            
        elif msg == DISCONNECT_MESSAGE:
            connected = False
            print(f"[DESCONECTADO] {addr}.")
            print(f"[THREADS ATIVAS] Usuários conectados: {threading.active_count() - 2}")
            send(conn, "Desconectando...");
            conn.close()
            return
        else:
            conn.send("Você está conectado no servidor!".encode(FORMAT))
        

def start():
    server.listen()
    print(f"[SERVIDOR CONECTADO] Servidor está conectado {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[THREADS ATIVAS] Usuários conectados: {threading.active_count() - 1}")

print("[STARTING] servidor está iniciando...")
start()
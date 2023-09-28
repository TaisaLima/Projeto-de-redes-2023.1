#!/usr/bin/python3 

import socket

HEADER = 2048
PORT = 12000
FORMAT = 'utf-8'
SERVER = '127.0.0.1'
DISCONNECT_MESSAGE = "!EXIT"
ADDR = (SERVER, PORT)
print(ADDR)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def get():
    return client.recv(HEADER).decode(FORMAT) 

def controller(msg):
    try:
        
        send(msg)
        res = get()

        if msg == DISCONNECT_MESSAGE:
            exit()
            print(res)
            return True

        if res == "Nome do arquivo: ":
            name = input(res)
            send(name)
            print(get())
        else:
            print(res)
    except:
        print("Servidor indisponivel, fechando conexão!")
        client.close();
        return True

        return False

def exit():
    client.close()
    return


while True:
    msg = input(f"Digite {DISCONNECT_MESSAGE} para finalizar a conexão: ")
    if controller(msg):
        break
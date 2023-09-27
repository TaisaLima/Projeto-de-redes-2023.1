#!/usr/bin/python3 

import socket
import threading

HEADER = 2048
PORT = 12000
SERVER = ""
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!EXIT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def fat (num):
    if num <= 0: 
        return 1
    
    return num * fat (num - 1)

def is_prime (num):
    i = 1
    prime = 1

    while i <= num ** 1/2:
        if num % i == 0:
            prime += 1
        i += 1

    if (prime == 2):
        return True
    else:
        return False

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
        if msg.lower() == "fatorial":
            send(conn, "Digite um número: ")
            msg = get(conn)
            print(f"[{addr} fatorial:{msg}]")
            try:
                msg = int(msg)
                if (msg >= 0):
                    send(conn, f"Fatorial de {msg} é igual {fat(msg)}")
                else:
                    send(conn, f"Digite um número maior que ou igual a 0")
            except:
                send(conn, "Você não digitou um número!");
        elif msg.lower() == "primo":
            send(conn, "Digite um número: ")
            msg = get(conn)
            print(f"[{addr} primo:{msg}]")
            try:
                msg = int(msg)
                if msg >= 2:
                    if is_prime(msg):
                        send(conn, f"{msg} é primo!")
                    else:
                        send(conn, f"{msg} não é primo!")
                else:
                    send(conn, f"Digite um número maior que ou igual a 2!")
            except:
                send(conn, "Você não digitou um número!");
        elif msg.lower() == "par":
            send(conn, "Digite um número: ")
            msg = get(conn)
            print(f"[{addr} par:{msg}]")
            try:
                msg = int(msg)
                if msg % 2 == 0:
                        send(conn, f"{msg} é número par!")
                else:
                    send(conn, f"{msg} é número ímpar!")
            except:
                send(conn, "Você não digitou um número!");
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
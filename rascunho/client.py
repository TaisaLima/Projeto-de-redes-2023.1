
import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4457
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cliente.connect(ADDR)

    arquivo = open("Hello.txt", "r")
    dados = arquivo.read()

    cliente.send("Hello.txt".encode(FORMAT))
    mensagem = cliente.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {mensagem}")

    cliente.send(dados.encode(FORMAT))
    mensagem = cliente.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {mensagem}")

    arquivo.close()

    cliente.close()


if __name__ == "__main__":
    main()

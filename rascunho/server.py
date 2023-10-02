
import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4457
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

def main():
    print("O servidor está iniciando")
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("O servidor está aguardando")

    while True:

        conn, addr = server.accept()
        print(f"[Nova Conexão] {addr} conectado.")

        NomeArquivo  = conn.recv(SIZE).decode(FORMAT)
        print(f"Processando o nome do arquivo...")
        arquivo = open(NomeArquivo, "w")
        conn.send("Nome do arquivo recebido com sucesso!".encode(FORMAT))

        dados = conn.recv(SIZE).decode(FORMAT)
        print(f"Processando dados do arquivo...")
        arquivo.write(dados)
        conn.send("Arquivo recebido com sucesso".encode(FORMAT))

        arquivo.close()

        conn.close()
        print(f"[Desconectado] {addr} se desconectou.")

if __name__ == "__main__":
    main()

import socket
import os
import threading


def receive_files(conn):

    # CONFIRMAR ARQUIVO
    try:
        confirm = conn.recv(4096).rstrip().decode()
        file_name = confirm.split(":")[-1]
        file_size = int(confirm.split(":")[0])

    except Exception as e:
        print("\nErro na confirmacao:", e)
        return

    aux_size = file_size
    # CASO JA EXISTA UM ARQUIVO DE MESMO NOME NA PASTA
    aux_name = file_name
    i = 1
    while os.path.exists("../dados/" + aux_name):
        aux_name = '(' + str(i) + ') ' + file_name
        i += 1

    file_name = aux_name

    # BAIXANDO ARQUIVO
    with open("../dados/" + file_name, 'wb') as file:
        while True:
            if aux_size <= 0:
                break

            try:
                byte = conn.recv(1024)
                file.write(byte)
                aux_size -= len(byte)

            except Exception as e:
                print("\nErro no download:", e)
                return

    print("\nArquivo adicionado com sucesso!")


def list_files(conn):

    files = os.listdir(os.path.join(os.getcwd(), "../dados"))
    options = "Opções de download:\n"
    i = 1

    for item in files:
        options += str(i) + ". " + item + "\n"
        i += 1

    try:
        conn.sendall(str.encode(options))
    except Exception as e:
        print("Erro no envio:", e)


def send_files(conn):
    files = os.listdir(os.path.join(os.getcwd(), "../dados"))

    # RECEBENDO OPCAO
    try:
        resp_option = int(conn.recv(1024).rstrip().decode())
        file_size = os.path.getsize(
            "../dados/" + files[resp_option-1])
        confirm = str(file_size) + ":" + \
            str(files[resp_option-1])
        conn.sendall(confirm.encode())

    except Exception as e:
        print("Erro no recebimento de dados:", e)
        return

    # ENVIANDO ARQUIVO
    try:
        choosed_file = open(
            "../dados/" + str(files[resp_option-1]), "rb")

        while True:
            file_in_bytes = choosed_file.read(1024)
            if len(file_in_bytes) <= 0:
                # FINALIZOU O ARQUIVO
                break
            conn.sendall(file_in_bytes)

    except Exception as e:
        print("Erro no envio de dados:", e)


def client_control(conn, client_addr):

    while True:
        option = conn.recv(1024).decode()

        if option == "upload":
            receive_files(conn)

        elif option == "to_list":
            list_files(conn)

        elif option == "download":
            send_files(conn)

        elif option == "exit":
            conn.close()
            break


def servidor():

    server_addr = ("localhost", 12345)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(server_addr)
    server_socket.listen(5)

    print("\nEscutando em", server_addr)

    while True:

        # NOVA CONEXAO
        conn, client_addr = server_socket.accept()
        print("\nNova conexao recebida de ", client_addr)

        # ADICIONANDO THREAD
        thread = threading.Thread(
            target=client_control, args=(conn, client_addr))
        thread.start()

        print("Conexoes ativas:", threading.active_count()-1)


if __name__ == "__main__":
    servidor()

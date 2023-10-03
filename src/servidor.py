import socket
import os
import threading


def receive_files(conn):

    # CONFIRMAR ARQUIVO ATRAVÉS DO CLIENTE
    try:
        confirm = conn.recv(4096).rstrip().decode() #RECEBE A CONFIRMAÇÃO
        file_name = confirm.split(":")[-1] #PEGA O NOME DO ARQUIVO
        file_size = int(confirm.split(":")[0]) #PEGA O TAMANHO DO ARQUIVO

    except Exception as error: #EXCEÇÃO CASO O ARQUIVO NÃO SEJA ENCONTRADO
        print("\nErro na confirmacao:", error)
        return

    aux_size = file_size
    # OCORRÊNCIA DE ARQUIVOS DE MESMO NOME
    aux_name = file_name
    i = 1
    while os.path.exists("../dados/" + aux_name):
        aux_name = '(' + str(i) + ') ' + file_name #ADICIONA PARÊNTESIS 
        i += 1

    file_name = aux_name

    # REALIZANDO O DOWNLOAD DO ARQUIVO
    with open("../dados/" + file_name, 'wb') as file:
        while True: #LAÇo PARA A BAIXAR O ARQUIVO
            if aux_size <= 0:
                break

            try:
                byte = conn.recv(1024)
                file.write(byte)
                aux_size -= len(byte)

            except Exception as error:
                print("\nErro no download:", error)
                return

    print("\nArquivo adicionado com sucesso!")


def list_files(conn): #FUNÇÃO PARA LISTAR OS ARQUIVOS DENTRO DO DIRETÓRIO

    files = os.listdir(os.path.join(os.getcwd(), "../dados")) #LISTA OS ARQUIVOS
    options = "Opções de download:\n"
    i = 1

    for item in files:
        options += str(i) + ". " + item + "\n"
        i += 1

    try:
        conn.sendall(str.encode(options)) #ENVIA A LISTA DE ARQUIVOS COMO UMA STRING
    except Exception as error:
        print("Erro no envio:", error)


def send_files(conn): #FUNÇÃO PARA ENVIAR OS ARQUIVOS
    files = os.listdir(os.path.join(os.getcwd(), "../dados")) #LISTA OS ARQUIVOS EM UM VETOR

    # RECEBENDO OPCAO
    try:
        resp_option = int(conn.recv(1024).rstrip().decode()) #RECEBE A OPÇÃO ESCOLHIDA PELO CLIENTE
        file_size = os.path.getsize(
            "../dados/" + files[resp_option-1])
        confirm = str(file_size) + ":" + \       
            str(files[resp_option-1])
        conn.sendall(confirm.encode())#ENVIA A CONFIRMAÇÃO DO ARQUIVO

    except Exception as error:
        print("Erro no recebimento de dados:", error)
        return

    # ENVIANDO ARQUIVO
    try:
        choosed_file = open(
            "../dados/" + str(files[resp_option-1]), "rb") #ESCOLHE O ARQUIVO

        while True:
            file_in_bytes = choosed_file.read(1024) #LÊ E ENVIA CADA BYTE DOS ARQUIVOS
            if len(file_in_bytes) <= 0:
                # FINALIZOU O ARQUIVO
                break
            conn.sendall(file_in_bytes) # ENVIA O BYTE

    except Exception as error:
        print("Erro no envio de dados:", error)


def client_control(conn, client_addr): #MENU

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

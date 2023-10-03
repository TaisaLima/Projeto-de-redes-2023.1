import socket
import os


def list_files(conn): #DISPLAY

    print()
    try:
        list_files = str(conn.recv(4096).rstrip().decode()) #LISTA OS ARQUIVOS PARA SEREM RECEBIDOS
        print(list_files)
        input("\nPressione enter...")

    except Exception as error:
        print("\nErro em obter opções:", error)
        return


def upload(conn): #UPLOAD
    
    # LISTANDO ARQUIVOS DISPONIVEIS PARA ENVIO 
    files = os.listdir(os.path.join(os.getcwd(), "../dados cliente"))

    options = "\nOpções de envio:\n"
    i = 1
    
    for item in files:
        options += str(i) + ". " + item + "\n"
        i += 1 
    print(options)

    # ESCOLHENDO ARQUIVO A SER ENVIADO
    choosed_id = int(input("Digite o ID do arquivo a ser enviado: "))

    
    # CONFIRMANDO ARQUIVO COM O SERVIDOR
    try:
        file_name = files[choosed_id-1] #SELECIONA O ARQUIVO NO ARRAY DE ARQUIVOS
        file_size = os.path.getsize("../dados cliente/" + files[choosed_id-1]) #SELECIONA O CAMINHO NO DIRETÓRIO

        confirm = str(file_size) + ":" + str(file_name) #CONFIRMA O ARQUIVO
        conn.sendall(confirm.encode()) #ENVIA O ARQUIVO

        print("\nEnviando o arquivo:", file_name)

    except Exception as error:
        print("Erro na escolha do arquivo:", error)
        return


    # ENVIANDO ARQUIVO
    try:
        choosed_file = open("../dados cliente/" + file_name, "rb") #SELECIONA O ARQUIVO PARA SER ENVIADO
        
        while True:
            file_in_bytes = choosed_file.read(1024) #Lê O ARQUIVO
            if len(file_in_bytes) <= 0:
                # FINALIZOU O ARQUIVO
                break
            conn.sendall(file_in_bytes) #ENVIA OS BYTES DO ARQUIVO

    except Exception as error:
        print("\nErro de dados:", error)
        return 

    print("\nArquivo enviado!")   
    input("Pressione enter para continuar...")



def download(conn):
    
    # COMANDO
    print()
    choosed_id = input("Digite o número do arquivo escolhido (disponiveis na listagem): ")
    
    # ENVIANDO option
    try:
        conn.send(choosed_id.encode())

    except Exception as error:
        print("\nErro:", error)
        return

    # confirm ARQUIVO
    try:
        confirm = conn.recv(4096).rstrip().decode() #RECEBE A CONFIRMAÇÃO DE RECEBIMENTO
        file_name = confirm.split(":")[-1] #LÊ O NOME DO ARQUIVO
        file_size = int(confirm.split(":")[0]) #PEGA O TAMANHO DO ARQUIVO
        
        print(file_name)

    except Exception as error:
        print("\nErro na confirmação:", error)
        return

    # OCORRÊNCIA DE ARQUIVOS DE MESMO NOME
    aux_name = file_name
    i = 1
    while os.path.exists("./dados cliente/" + aux_name):
        aux_name = '(' + str(i) + ')' + file_name
        i += 1

    file_name = aux_name
    aux_size = file_size

    # BAIXANDO ARQUIVO
    try:
        file = open("../dados cliente/" + file_name, 'wb') #ENTRA NA PASTA E USA O WB PARA ESCREVER
    except Exception as error:
        print("Erro na obtenção do arquivo:", error)
        return

    while True:
        if aux_size <= 0: #ENQUANTO A QUANTIDADE DE BYTES RECEBIDOS NÃO CHEGAR EM ZERO
            break

        try:
            byte = conn.recv(1024) #RECEBE O BYTE DO SERVIDOR
            file.write(byte) #ESCREVE O ARQUIVO NO DIRETÓRIO ESCOLHIDO
            aux_size -= len(byte) #DIMINUI A QUANTIDADE DE BYTES

        except Exception as error:
            print("Erro no download:", error)
            return

    print("Arquivo baixado!")

            

def client():

    addr = ("localhost", 12345)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(addr)

    while True:

        # MENU
        print('\n[1] Listar arquivos\n[2] Enviar arquivo\n[3] Receber arquivo\n[4] Sair\n')
        option = input("Opção: ")
        
        if option == '1':
            try:
                server_socket.send("to_list".encode())
            except Exception as error:
                print("Erro:", error)
                server_socket.close()
                break

            error = list_files(server_socket)
            if error:
                server_socket.close()
                break

        elif option == '2':
            try:
                server_socket.send("upload".encode())
            except Exception as error:
                print("Erro:", error)
                server_socket.close()
                break

            error = upload(server_socket)
            if error:
                server_socket.close()
                break

        elif option == '3':
            try:
                server_socket.send("download".encode())
            except Exception as error:
                print("Erro:", error)
                server_socket.close()
                break

            error = download(server_socket)
            if error:
                server_socket.close()
                break

        elif option == '4':
            try:
                server_socket.send("exit".encode())
            except Exception as error:
                print("Erro:", error)

            server_socket.close()
            break
        else:
            print('Opção invalida!')


if __name__ == "__main__":
    client()

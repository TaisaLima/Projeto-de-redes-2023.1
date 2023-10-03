import socket
import os


def list_files(conn):

    print()
    try:
        list_files = str(conn.recv(4096).rstrip().decode())
        print(list_files)
        input("\nPressione enter...")

    except Exception as e:
        print("\nErro em obter opções:", e)
        return


def upload(conn):
    
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
        file_name = files[choosed_id-1]
        file_size = os.path.getsize("../dados cliente/" + files[choosed_id-1])

        confirm = str(file_size) + ":" + str(file_name)
        conn.sendall(confirm.encode())

        print("\nEnviando o arquivo:", file_name)

    except Exception as e:
        print("Erro na escolha do arquivo:", e)
        return


    # ENVIANDO ARQUIVO
    try:
        choosed_file = open("../dados cliente/" + file_name, "rb")
        
        while True:
            file_in_bytes = choosed_file.read(1024)
            if len(file_in_bytes) <= 0:
                # FINALIZOU O ARQUIVO
                break
            conn.sendall(file_in_bytes)

    except Exception as e:
        print("\nErro de dados:", e)
        return 

    print("\nArquivo enviado!")   
    input("Pressione enter para continuar...")



def download(conn):
    
    # COMANDO
    print()
    choosed_id = input("Digite o número do arquivo escolhido: ")
    
    # ENVIANDO option
    try:
        conn.send(choosed_id.encode())

    except Exception as e:
        print("\nErro:", e)
        return

    # confirm ARQUIVO
    try:
        confirm = conn.recv(4096).rstrip().decode()
        file_name = confirm.split(":")[-1]
        file_size = int(confirm.split(":")[0])
        
        print(file_name)

    except Exception as e:
        print("\nErro na confirmação:", e)
        return

    # CASO JA EXISTA UM ARQUIVO DE MESMO NOME NA PASTA
    aux_name = file_name
    i = 1
    while os.path.exists("./dados cliente/" + aux_name):
        aux_name = '(' + str(i) + ')' + file_name
        i += 1

    file_name = aux_name
    aux_size = file_size

    # BAIXANDO ARQUIVO
    try:
        file = open("../dados cliente/" + file_name, 'wb')
    except Exception as e:
        print("Erro na obtenção do arquivo:", e)
        return

    while True:
        if aux_size <= 0:
            break

        try:
            byte = conn.recv(1024)
            file.write(byte)
            aux_size -= len(byte)

        except Exception as e:
            print("Erro no download:", e)
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
            except Exception as e:
                print("Erro:", e)
                server_socket.close()
                break

            error = list_files(server_socket)
            if error:
                server_socket.close()
                break

        elif option == '2':
            try:
                server_socket.send("upload".encode())
            except Exception as e:
                print("Erro:", e)
                server_socket.close()
                break

            error = upload(server_socket)
            if error:
                server_socket.close()
                break

        elif option == '3':
            try:
                server_socket.send("download".encode())
            except Exception as e:
                print("Erro:", e)
                server_socket.close()
                break

            error = download(server_socket)
            if error:
                server_socket.close()
                break

        elif option == '4':
            try:
                server_socket.send("exit".encode())
            except Exception as e:
                print("Erro:", e)

            server_socket.close()
            break
        else:
            print('Opção invalida!')


if __name__ == "__main__":
    client()

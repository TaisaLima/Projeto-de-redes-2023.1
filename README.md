# ✔️ PROJETO SOCKETS

Projeto da disciplina Redes de Computadores (UFAL), ministrada pelo professor Leandro de Sales, o qual se trata da implementação de aplicação em redes por meio de sockets.

Alunas:

- Leticia Gabriela Cena de Lima
- Maria Fernanda Herculano Machado da Silva

## Como executar? 💻

A aplicação foi desenvolvida na linguagem Python, portanto é preciso que na máquina que deseje executar exista uma versão recente do Python, e.g. 3.9.x.  
Para executar, é preciso baixar o repositório e abrir a pasta "src".  
Feito isso, abrir o terminal na mesma pasta e executar o comando:

```
$ python3 servidor.py
```

Assim, o servidor já estará conectado e pronto para receber os comandos do cliente.  
Para que o cliente possa começar a interagir com o servidor é executado o seguinte comando, em uma nova aba do terminal (na mesma pasta "src"):

```
$ python3 cliente.py
```

Irá abrir uma lista de opções que o cliente poderá escolher: listar os arquivos do servidor, baixar e enviar arquivos.  
Por causa do uso de thread, é possível que mais de um cliente se conecte ao servidor ao mesmo tempo, para testar isso é só repetir o último passo em outra aba do terminal.

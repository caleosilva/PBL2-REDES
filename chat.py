import module
import socket
import threading
import json
import time
from queue import Queue


'''
Variávis de controle do código.
'''
HOST_LISTEN = "127.0.0.1"
data_users = [
    {"host": HOST_LISTEN, "port": 1111, "nome": "jose"},
    {"host": HOST_LISTEN, "port": 2222, "nome": "maria"},
    {"host": HOST_LISTEN, "port": 3333, "nome": "rebeca"}
]
my_info = {'host': HOST_LISTEN, 'port': '', 'nome': ''}
mi_redes = []


'''
Objeto que implementa o relógio lógico de Lamport.
'''
class LamportClock:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1
            return self.value

    def update(self, received_time):
        with self.lock:
            self.value = max(self.value, received_time) + 1
            return self.value


'''
Função que roda em uma thread e é responsável por receber as mensagens e colocá-las em uma fila 
a fim de serem processadas.
'''
def server(message_queue):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_adress = (my_info['host'], my_info['port'])
    server_socket.bind(server_adress)

    while True:
        data, client_address = server_socket.recvfrom(1024)
        dataObj = json.loads(data)
        message_queue.put(dataObj)

'''
Função que roda em uma thread e é responsável por pegar as solicitações da fila e
processá-las.
'''
def handle_request(message_queue, clock):
    while True:
        message = message_queue.get()

        try:
            if message['type'] == 'msg':
                clock.update(message['time'])
                module.handle_mensagem(message, mi_redes, my_info)
            elif message['type'] == 'sync_clock':
                objIndentificador = {'type': 'sync_clock_response', 'time': clock.value, 'sender': my_info}
                module.responde_message(objIndentificador, my_info, message['sender'])
            elif message['type'] == 'sync_clock_response':
                module.sync_clock(clock, message)

        except Exception as e:
            print("Erro ao lidar com o request:", e)


'''
Função que roda em uma thread e é responsável sincronizar o relógio com todos os usuários online.
'''
def send_clock_to_sync(clock):
    objIndentificador = {'type': 'sync_clock', 'time': clock.value, 'sender': my_info}
    module.send_message(objIndentificador, my_info, data_users)

'''
Função que roda em uma thread e é responsável por controlar as mensagens de um usuário, mandando 
para os demais e adicionando em sua lista.
'''
def write_prepare_message(clock):
    while True:
        mensagem = input("")

        if (mensagem != ""):

            # Cria o objeto da mensagem
            id_message = module.generete_id()
            objMsg = {'type': 'msg', 'time': clock.value, 'id': id_message, 'msg': mensagem, 'sender': my_info}

            # Envia a mensagem para a lista de mensagens local
            module.handle_mensagem(objMsg, mi_redes, my_info)

            # Envie a mensagem para outros usuários
            module.send_message(objMsg, my_info, data_users)

            # Atualiza o relógio
            clock.increment()
            

def sync_messages():
    # 1- Mandar minha lista para todos.
    # 2- Receber a lista de todos
    # 3- Unir as listas
    pass


'''
Função responsável por identificar o usuário e realizar o "LOGIN".
'''
def main():
    print('-=-=-=-= BEM VINDO =-=-=-=-\n\n')

    print('[1] -> Login')
    print('[2] -> Sair\n')

    opc = input("-> ")

    if opc == '1':
        port = input("\nDigite a porta: ")
        nome = input("Digite o nome: ")
        my_info['port'] = int(port)
        my_info['nome'] = nome

        
        start()
        module.show_messages(mi_redes, my_info)

    elif opc == '2':
        exit()

'''
Função responsável por instanciar os objetos e iniciar as threads.
'''
def start():
    clock = LamportClock()
    message_queue = Queue()

    sync_clock_thread = threading.Thread(target=send_clock_to_sync, args=(clock,))
    sync_clock_thread.start()



    server_thread = threading.Thread(target=server, args=(message_queue,))
    server_thread.start()

    handle_request_thread = threading.Thread(target=handle_request, args=(message_queue, clock))
    handle_request_thread.start()

    write_prepare_message_thread = threading.Thread(target=write_prepare_message, args=(clock,))
    write_prepare_message_thread.start()


if __name__ == "__main__":
    main()

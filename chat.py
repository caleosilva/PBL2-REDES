import module
import socket
import threading
import json
import time
import random
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
        # print("data no server: ", data, '\n\n')
        dataObj = json.loads(data)
        message_queue.put(dataObj)

'''
Função que roda em uma thread e é responsável por pegar as solicitações da fila e
processá-las.
'''
def handle_request(message_queue, clock, dict_sync_queue):
    while True:
        message = message_queue.get()

        # print("\nhandle_request: ", message, '\n')

        try:
            if message['type'] == 'msg':
                clock.update(message['time'])
                module.handle_mensagem(message, mi_redes, my_info)
            elif message['type'] == 'sync_clock':
                objIndentificador = {'type': 'sync_clock_response', 'time': clock.value, 'sender': my_info}
                module.responde_message(objIndentificador, my_info, message['sender'])
            elif message['type'] == 'sync_clock_response':
                module.sync_clock(clock, message)
            elif message['type'] == 'sync_list_request':
                print("Recebi o pedido de envio da minha lista")
                module.send_message_list(mi_redes, my_info, data_users)
            elif message['type'] == 'sync_list_response':
                dict_sync_queue.put(message)
                # print("Adicionei a msg na fila")

        except Exception as e:
            print("Erro ao lidar com o request:", e)

'''
Função que roda em uma thread e é responsável sincronizar o relógio com todos os usuários online.
'''
def ask_sync_clock_and_list(clock):
    objIndentificadorLista = {'type': 'sync_list_request', 'sender': my_info}
    module.send_message(objIndentificadorLista, my_info, data_users)

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
            # Atualiza o relógio
            clock.increment()

            # Cria o objeto da mensagem
            id_message = module.generete_id()
            objMsg = {'type': 'msg', 'time': clock.value, 'id': id_message, 'msg': mensagem, 'sender': my_info}

            # Envia a mensagem para a lista de mensagens local
            module.handle_mensagem(objMsg, mi_redes, my_info)

            # Envie a mensagem para outros usuários
            module.send_message(objMsg, my_info, data_users)



# def send_messageList_sync(my_list):
#     id_lista = ''.join(str(random.randint(1, 100)) for _ in range(6))
#     module.send_message_list(my_list, my_info, data_users, id_lista)

# falta adicionar a propria lista a isso
def receive_dict_sync(dict_sync_queue):
    
    dict_sync = {}
    while True:
        item_dict = dict_sync_queue.get()

        id_list = item_dict['id_list']
        if id_list in dict_sync:
            dict_sync[id_list].append(item_dict)
        else:
            dict_sync[id_list] = [item_dict]

        # module.organize_message_dict(item_dict, dict_sync)
        verificacao = module.check_full_dict(dict_sync)

        # Falta comparar com sua prórpia lista
        if (verificacao):
            new_list = module.extrair_e_ordenar_mensagens(dict_sync)
            mi_redes = new_list
            module.show_messages(mi_redes, my_info)
            dict_sync.clear()

            


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
    dict_sync_queue = Queue()

    sync_clock_and_list_thread = threading.Thread(target=ask_sync_clock_and_list, args=(clock,))
    sync_clock_and_list_thread.start()

    receive_dict_sync_thread = threading.Thread(target=receive_dict_sync, args=(dict_sync_queue,))
    receive_dict_sync_thread.start()

    server_thread = threading.Thread(target=server, args=(message_queue,))
    server_thread.start()

    handle_request_thread = threading.Thread(target=handle_request, args=(message_queue, clock, dict_sync_queue))
    handle_request_thread.start()

    write_prepare_message_thread = threading.Thread(target=write_prepare_message, args=(clock,))
    write_prepare_message_thread.start()

if __name__ == "__main__":
    main()

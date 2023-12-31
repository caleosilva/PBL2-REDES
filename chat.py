import module
import socket
import threading
import json
import time
from queue import Queue


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
def server(message_queue, my_info):
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
def handle_request(message_queue, clock, dict_sync_queue, mi_redes, my_info, data_users):
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
                clock.update(message['time'])
            elif message['type'] == 'sync_list_request':
                module.send_message_list(mi_redes, my_info, data_users)
            elif message['type'] == 'sync_list_response':
                dict_sync_queue.put(message)
        except Exception as e:
            print("Erro ao lidar com o request:", e)

'''
Função que roda em uma thread e é responsável sincronizar o relógio com todos os usuários online.
'''
def ask_sync_clock_and_list(clock, my_info, data_users):
    objIndentificador = {'type': 'sync_clock', 'time': clock.value, 'sender': my_info}
    confirmacao = module.send_message(objIndentificador, my_info, data_users)

    if confirmacao:
        objIndentificadorLista = {'type': 'sync_list_request', 'sender': my_info}
        module.send_message(objIndentificadorLista, my_info, data_users)

'''
Função que roda em uma thread e é responsável por controlar as mensagens de um usuário, mandando 
para os demais e adicionando em sua lista.
'''
def write_prepare_message(clock, mi_redes, my_info, data_users):
    while True:
        mensagem = input("")
        if (mensagem != ""):
            clock.increment()
            objMsg = {'type': 'msg', 'time': clock.value, 'id': module.generete_id(), 'msg': module.criptografar(mensagem), 'sender': my_info}
            module.handle_mensagem(objMsg, mi_redes, my_info)
            module.send_message(objMsg, my_info, data_users)

'''
Função que roda em uma thread e é responsável por receber e tratar as mensagens de sincronização.
'''
def receive_dict_sync(dict_sync_queue, mi_redes, my_info, clock):    
    while True:
        item_dict = dict_sync_queue.get()
        new_id = item_dict['body']['id']

        if (not module.is_duplicate_message(new_id, mi_redes)):
            mi_redes.append(item_dict['body'])
            mi_redes.sort(key=lambda x: (x['time'], x['id']))
            module.show_messages(mi_redes, my_info)
            module.fix_uknown_error_sync(mi_redes, clock)

'''
Função que roda em uma thread e é responsável por sincronizar as listas a cada 10 segundos
'''
def sync_active(mi_redes, my_info, data_users):
    while True:
        if len(mi_redes) > 0:
            # print("sync_active")
            objIndentificadorLista = {'type': 'sync_list_request', 'sender': my_info}
            module.send_message(objIndentificadorLista, my_info, data_users)
            time.sleep(10)

'''
Função responsável por identificar o usuário e realizar o "LOGIN".
'''
def main():
    data_users = [
        {"host": '172.16.103.1', "port": 1111, "nome": "Amancio"},
        {"host": '172.16.103.2', "port": 2222, "nome": "Augusto"},
        {"host": '172.16.103.3', "port": 3333, "nome": "Joao"},
        {"host": '172.16.103.4', "port": 4444, "nome": "Maria"},
        {"host": '172.16.103.5', "port": 5555, "nome": "Leo"},
        {"host": '172.16.103.6', "port": 6666, "nome": "Lucia"},
        {"host": '172.16.103.7', "port": 7777, "nome": "Carlos"},
        {"host": '172.16.103.8', "port": 8888, "nome": "Ana"},
        {"host": '172.16.103.9', "port": 9999, "nome": "Pedro"},
        {"host": '172.16.103.10', "port": 1010, "nome": "Isabela"}  
    ]
    
    my_info = {'host': '', 'port': '', 'nome': ''}
    mi_redes = []

    print('-=-=-=-= BEM VINDO =-=-=-=-\n\n')

    print('[1] -> Login')
    print('[2] -> Sair\n')

    opc = input("-> ")

    if opc == '1':
        print("\nUsuários:")
        for i, user in enumerate(data_users):
            print(f"{i + 1}. {user['nome']} - ({user['host']}:{user['port']})")

        try:
            escolha = int(input("\nDigite o número correspondente ao usuário desejado: "))
            if 1 <= escolha <= len(data_users):
                selected_user = data_users[escolha - 1]
                my_info['host'] = selected_user['host']
                my_info['port'] = selected_user['port']
                my_info['nome'] = selected_user['nome']

                start(mi_redes, my_info, data_users)
                module.show_messages(mi_redes, my_info)
            else:
                print("Escolha inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

    elif opc == '2':
        exit()

'''
Função responsável por instanciar os objetos e iniciar as threads.
'''
def start(mi_redes, my_info, data_users):
    clock = LamportClock()
    message_queue = Queue()
    dict_sync_queue = Queue()

    sync_clock_and_list_thread = threading.Thread(target=ask_sync_clock_and_list, args=(clock, my_info, data_users))
    sync_clock_and_list_thread.start()

    receive_dict_sync_thread = threading.Thread(target=receive_dict_sync, args=(dict_sync_queue, mi_redes, my_info, clock))
    receive_dict_sync_thread.start()

    server_thread = threading.Thread(target=server, args=(message_queue, my_info))
    server_thread.start()

    handle_request_thread = threading.Thread(target=handle_request, args=(message_queue, clock, dict_sync_queue, mi_redes, my_info, data_users))
    handle_request_thread.start()

    write_prepare_message_thread = threading.Thread(target=write_prepare_message, args=(clock, mi_redes, my_info, data_users))
    write_prepare_message_thread.start()

    sync_active_thread = threading.Thread(target=sync_active, args=(mi_redes, my_info, data_users))
    sync_active_thread.start()

if __name__ == "__main__":
    main()

import module
import socket
import threading
import json
import time
from queue import Queue



HOST_LISTEN = "127.0.0.1"

data_users = [
    {"host": HOST_LISTEN, "port": 1111, "nome": "jose"},
    {"host": HOST_LISTEN, "port": 2222, "nome": "maria"},
    {"host": HOST_LISTEN, "port": 3333, "nome": "rebeca"}
]

my_info = {'host': HOST_LISTEN, 'port': '', 'nome': ''}

mi_redes = [
    
]

# Relógio lógico
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


# Ouvido
def server(clock, message_queue):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_adress = (my_info['host'], my_info['port'])
    server_socket.bind(server_adress)

    while True:
        data, client_address = server_socket.recvfrom(1024)
        dataObj = json.loads(data)
        print('\n', dataObj)
        print(f"Received: {dataObj['msg']} at Lamport time {clock.value}\n")

        clock.update(dataObj['time'])


        message_queue.put(dataObj)

def handle_request(message_queue):
    while True:
        message = message_queue.get()
        print(f"Processing: {message['msg']} at Lamport time {message['time']}")

        try:
            if message['type'] == 'sync':
                # list_messages = module.recv_message_list(message, client_address, list_sync)
                pass
            elif message['type'] == 'msg':
                module.handle_mensagem(message, mi_redes, my_info)
            elif message['type'] == 'on-sync':
                pass
        except Exception as e:
            print("Erro ao lidar com o request:", e)



def sync_messages():
    # Exibe as mensagens
    module.show_messages(mi_redes, my_info)

# Manda mensagens
def write_prepare_message(clock):
    while True:
        mensagem = input("")

        if (mensagem != ""):

            lamport_time = clock.increment()
            id_message = module.generete_id()

            objMsg = {'type': 'msg', 'time': lamport_time, 'id': id_message, 'msg': mensagem, 'sender': my_info}
            
            #{'time': , 'id': '', 'msg': '', 'sender': {}},

            # ELE TÁ RECEBENDO TYPE E NÃO TA TRATANDO ANTES DE ADD NA LISTA, TENHO QUE ALTERAR ISSO !!!!!!!!!!!!!!

            # Envia a mensagem para a lista de mensagens local
            module.handle_mensagem(objMsg, mi_redes, my_info)

            # Envie a mensagem para outros usuários
            module.send_message(objMsg, my_info, data_users)
            
            # mandar a nova lista para todos os usuários online
            # module.send_message_list(mi_redes, my_info, data_users)

            # receber a lista de todos e sincronizar
    

# mudar a forma que o login está sendo feito
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

        module.clear_screen()
        start()
    elif opc == '2':
        exit()


def start():
    clock = LamportClock()
    message_queue = Queue()

    accept_thread = threading.Thread(target=sync_messages, args=())
    accept_thread.start()

    accept_thread = threading.Thread(target=server, args=(clock, message_queue))
    accept_thread.start()

    process_thread = threading.Thread(target=handle_request, args=(message_queue,))
    process_thread.start()



    accept_thread = threading.Thread(target=write_prepare_message, args=(clock,))
    accept_thread.start()


if __name__ == "__main__":
    main()

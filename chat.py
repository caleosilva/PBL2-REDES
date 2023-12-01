import module
import socket
import threading
import json


HOST_LISTEN = "10.0.0.103"

data_users = [
    {"host": HOST_LISTEN, "port": 1111, "nome": "jose"},
    {"host": HOST_LISTEN, "port": 2222, "nome": "maria"},
    {"host": HOST_LISTEN, "port": 3333, "nome": "rebeca"}
]

my_info = {'host': HOST_LISTEN, 'port': '', 'nome': ''}

mi_redes = [
    {'index': 1, 'id': '0d623e1a-1e0a-4c72-9455-e9268f880768', 'msg': 'Alguem online?',
        'sender': {"host": HOST_LISTEN, "port": 1111, "nome": "jose"}},
    {'index': 2, 'id': '07908719-c648-4e2e-ba1d-b176a897db78', 'msg': 'Aloo?',
        'sender': {"host": HOST_LISTEN, "port": 1111, "nome": "jose"}},
    {'index': 3, 'id': 'e28f3b19-386e-43b3-b030-22ef0269fb1e', 'msg': 'Oii, to aqui',
        'sender':     {"host": HOST_LISTEN, "port": 2222, "nome": "maria"}}
]


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_adress = (my_info['host'], my_info['port'])
    server_socket.bind(server_adress)

    print("Ouvindo em ", server_adress)

    while True:
        data, client_address = server_socket.recvfrom(1024)
        dataObj = json.loads(data)

        print("data: ", dataObj)    
        print("client_address: ", client_address)

        user_thread = threading.Thread(
            target=handle_request, args=(dataObj, client_address))
        user_thread.start()


def handle_request(dataObj, client_address):

    print(dataObj['type'])
    try:
        if dataObj['type'] == 'sync':
            print("Solicitiação de sync")
            # handle_sync_request(mensagemJson, user_socket)
        elif dataObj['type'] == 'msg':
            print('Vou adicionar')
            handle_mensagem(dataObj, mi_redes)

    except Exception as e:
        print("Erro ao lidar com o usuário:", e)


def handle_mensagem(objMsg, lista_mensagens):
    lista_mensagens.append(objMsg)
    show_messages(mi_redes)


def sync_messages():
    # Obtém o ID local
    # id_local = module.get_my_latest_index(mi_redes)

    # # Obtém o ID da última mensagem e o usuário atualizado
    # id_ultima_msg, userAtualizado = module.get_latest_id_and_user(
    #     data_users, my_info)

    # # Verifica se é necessário sincronizar
    # if module.check_need_sync(id_local, id_ultima_msg):
    #     try:
    #         # Abre um socket e conecta ao usuário atualizado
    #         user_socket = socket.socket()
    #         user_socket.connect(
    #             (userAtualizado['host'], userAtualizado['port']))

    #         # Cria uma mensagem de sincronização e a envia
    #         objMsg = {'header': 'sync', 'id_local': id_local}
    #         dadosMsn = json.dumps(objMsg)
    #         user_socket.send(dadosMsn.encode())

    #         # Recebe a lista sincronizada
    #         recv_list = module.recv_message_list(user_socket)
    #         print("sync_messages: ", recv_list)
    #         handle_update_list(mi_redes, recv_list)

    #     except Exception as e:
    #         print("Erro ao sincronizar mensagens:", e)
    #     finally:
    #         user_socket.close()

    # # Exibe as mensagens
    show_messages(mi_redes)


def send_messages():
    while True:
        mensagem = input("")

        if (mensagem != ""):
            # Obtém o último index local
            my_last_index = module.get_my_latest_index(mi_redes)

            # Gera o próximo ID da mensagem
            id_message = module.generete_id()
            index_message = 1
            if my_last_index:
                index_message = int(my_last_index) + 1

            # {
            # 'type: 'msg' || 'type: 'sync', 'size-list': 4
            # 'index': 3, 
            # 'id': 'e28f3b19-386e-43b3-b030-22ef0269fb1e', 
            # 'msg': 'Oii, to aqui',
            # 'sender': {"host": HOST_LISTEN, "port": 2222, "nome": "maria"}}

            objMsg = {'type': 'msg', 'index': index_message, 'id': id_message,
                      'msg': mensagem, 'sender': my_info}

            # Envia a mensagem para a lista de mensagens local
            handle_mensagem(objMsg, mi_redes)

            # Envie a mensagem para outros usuários
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            for user in data_users:
                if (my_info['port'] != user['port'] and my_info['nome'] != user['nome']):
                    print(user)
                    try:
                        client_socket.sendto(json.dumps(objMsg).encode(), (user['host'], user['port']))
                    except Exception as e:
                        print(e)
            
            # mandar a nova lista para todos os usuários online

            # receber a lista de todos e sincronizar


def show_messages(group_messages):
    # module.clear_screen()

    print(group_messages)

    print('--------------------------------------------------')
    print('|                   MI - REDES                   |')
    print('--------------------------------------------------\n\n')

    for dicionarioMensagem in group_messages:

        if (dicionarioMensagem['sender']['host'] == my_info['host'] and dicionarioMensagem['sender']['port'] == my_info['port']):
            print(
                f'\t\t{dicionarioMensagem["sender"]["nome"]} -> {dicionarioMensagem["msg"]}\n')
        else:
            print(
                f'{dicionarioMensagem["sender"]["nome"]} -> {dicionarioMensagem["msg"]}\n')


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
    accept_thread = threading.Thread(target=sync_messages, args=())
    accept_thread.start()

    accept_thread = threading.Thread(target=server, args=())
    accept_thread.start()

    accept_thread = threading.Thread(target=send_messages, args=())
    accept_thread.start()


if __name__ == "__main__":
    main()

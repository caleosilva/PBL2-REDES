import os
import json
import socket
import uuid


'''
Gera um ID único para a mensagem.
'''


def generete_id():
    return str(uuid.uuid4())


def get_my_latest_index(list_messages):
    last_id = False

    if (len(list_messages) > 0):
        last_id = list_messages[-1]['index']
    return last_id


'''
Limpa a tela tanto no linux quanto no windows
'''


def clear_screen():
    # Limpar a tela no Linux e macOS
    if os.name == 'posix':
        os.system('clear')

    # Limpar a tela no Windows
    elif os.name == 'nt':
        os.system('cls')


'''
Função responsável por retornar se um usuário precisa sincronizar ou não
'''


def check_need_sync(id_local, latest_id):
    if (id_local == ''):
        return True
    elif (int(latest_id) > int(id_local)):
        return True
    else:
        return False


'''
Retorna a chave pela qual uma lista de dicionario deve ser ordenada
'''


def sort_key(dic):
    return list(dic.keys())[0]

def send_message(objMsg, my_info, data_users):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for user in data_users:
        if (my_info['port'] != user['port'] and my_info['nome'] != user['nome']):
            try:
                client_socket.sendto(json.dumps(objMsg).encode(), (user['host'], user['port']))
            except Exception as e:
                print(e)

def send_message_list(message_list, my_info, data_users):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        for user in data_users:
            if my_info['port'] != user['port'] and my_info['nome'] != user['nome']:
                size_list = len(message_list)

                for objMsg in message_list:
                    objFormatado = {'size': size_list, 'type': 'sync', 'body': objMsg}
                    client_socket.sendto(json.dumps(objFormatado).encode(), (user['host'], user['port']))
                    
    except Exception as e:
        print("Erro durante o envio:", e)
    finally:
        # Fecha o socket após o envio
        client_socket.close()

def recv_message_list(user_address):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(user_address)

    list_message = []

    try:
        while True:
            data, client_address = server_socket.recvfrom(1024)
            received_message = json.loads(data.decode())
            print("Mensagem recebida:", received_message)

    except KeyboardInterrupt:
        print("Servidor encerrado pelo usuário.")
    finally:
        server_socket.close()

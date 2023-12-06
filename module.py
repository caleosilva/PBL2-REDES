import os
import json
import socket
import uuid


'''
Gera um ID único para a mensagem.
'''
def generete_id():
    return str(uuid.uuid4())

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

def responde_message(objMsg, my_info, info_user):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if (my_info['port'] != info_user['port'] and my_info['nome'] != info_user['nome']):
        try:
            client_socket.sendto(json.dumps(objMsg).encode(), (info_user['host'], info_user['port']))
        except Exception as e:
            print(e)

def send_message(objMsg, my_info, data_users):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for user in data_users:
        if (my_info['port'] != user['port'] and my_info['nome'] != user['nome']):
            try:
                client_socket.sendto(json.dumps(objMsg).encode(), (user['host'], user['port']))
            except Exception as e:
                print(e)

def show_messages(group_messages, my_info):
    clear_screen()

    print('--------------------------------------------------')
    print('|                   MI - REDES                   |')
    print('--------------------------------------------------\n\n')

    for dicionarioMensagem in group_messages:

        if (dicionarioMensagem['sender']['host'] == my_info['host'] and dicionarioMensagem['sender']['port'] == my_info['port']):
            print(
                f'\t\t({dicionarioMensagem["time"]}) {dicionarioMensagem["sender"]["nome"]} -> {dicionarioMensagem["msg"]}\n')
        else:
            print(
                f'({dicionarioMensagem["time"]}) {dicionarioMensagem["sender"]["nome"]} -> {dicionarioMensagem["msg"]}\n')

def handle_mensagem(objMsg, lista_mensagens, my_info):
    copia = (objMsg.copy())
    copia.pop('type')

    lista_mensagens.append(copia)
    show_messages(lista_mensagens, my_info)

def send_clock_to_sync(clock, my_info, data_users):
    objIndentificador = {'type': 'sync_clock', 'time': clock.value}
    send_message(objIndentificador, my_info, data_users)

def sync_clock(clock, info):
    try:
        clock_received = int(info['time'])
        if (clock_received > clock.value):
            clock.update(info['time'])
    except Exception as e:
        print(e)








def send_message_list(message_list, my_info, data_users, id_list):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        size_list = len(message_list)

        for user in data_users:
            if my_info['port'] != user['port'] and my_info['nome'] != user['nome']:
                for objMsg in message_list:
                    objFormatado = {'id_list': id_list, 'size': size_list, 'type': 'sync_list', 'body': objMsg}
                    client_socket.sendto(json.dumps(objFormatado).encode(), (user['host'], user['port']))
                    
    except Exception as e:
        print("Erro durante o envio:", e)
    finally:
        client_socket.close()

def recv_message_list(dataObj, client_address, list_sync):
    try:
        
        list_sync.append()

        print("dataObj: ", dataObj)
        print("client_address: ", client_address)   
        print("\n\n")

    except KeyboardInterrupt:
        print("Servidor encerrado pelo usuário.")


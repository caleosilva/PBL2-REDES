import os
import json
import socket
import uuid
import random

SHIFT_AMOUNT = 5



def generete_id():
    return str(uuid.uuid4())

def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')

def responde_message(objMsg, my_info, info_user):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if (my_info['port'] != info_user['port'] and my_info['nome'] != info_user['nome']):
        try:
            client_socket.sendto(json.dumps(objMsg).encode(), (info_user['host'], info_user['port']))
        except Exception as e:
            print(e)
    client_socket.close()

def send_message(objMsg, my_info, data_users):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        success = False
        for user in data_users:
            if (my_info['port'] != user['port'] and my_info['nome'] != user['nome']):
                try:
                    client_socket.sendto(json.dumps(objMsg).encode(), (user['host'], user['port']))
                    success = True
                except Exception as e:
                    success = False
                    print(e)
        return success
    finally:
        client_socket.close()

def show_messages(group_messages, my_info):
    clear_screen()
    print('--------------------------------------------------')
    print('|                   MI - REDES                   |')
    print('--------------------------------------------------\n\n')
    for dicionarioMensagem in group_messages:
        if (dicionarioMensagem['sender']['host'] == my_info['host'] and dicionarioMensagem['sender']['port'] == my_info['port']):
            print(
                f'\t\t({dicionarioMensagem["time"]}) {dicionarioMensagem["sender"]["nome"]} -> {descriptografar(dicionarioMensagem["msg"])}\n')
        else:
            print(
                f'({dicionarioMensagem["time"]}) {dicionarioMensagem["sender"]["nome"]} -> {descriptografar(dicionarioMensagem["msg"])}\n')

def handle_mensagem(objMsg, lista_mensagens, my_info):
    copia = (objMsg.copy())
    copia.pop('type')
    lista_mensagens.append(copia)
    show_messages(lista_mensagens, my_info)

def is_duplicate_message(id_obj, message_list):
    for message in message_list:
        if message['id'] == id_obj:
            return True
    return False

def send_message_list(message_list, my_info, data_users):
    if len(message_list) > 0:
        id_lista = ''.join(str(random.randint(1, 100)) for _ in range(6))
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            size_list = len(message_list)
            
            for user in data_users:
                if my_info['port'] != user['port'] and my_info['nome'] != user['nome']:
                    for objMsg in message_list:
                        objFormatado = {'id_list': id_lista, 'size': size_list, 'type': 'sync_list_response', 'body': objMsg}
                        client_socket.sendto(json.dumps(objFormatado).encode(), (user['host'], user['port']))
        except Exception as e:
            print("Error during sending:", e)
        finally:
            client_socket.close() 

def criptografar(frase):
    mensagem = ""
    for i in frase:
        mensagem += chr (ord(i) + SHIFT_AMOUNT)
    return mensagem

def descriptografar(mensagem):
    frase = ""
    for i in mensagem:
        frase += chr (ord(i) - SHIFT_AMOUNT)
    return frase

def fix_uknown_error_sync(message_list, clock):
    maior_time = max(message_list, key=lambda x: x['time'])
    clock.update(maior_time['time'])


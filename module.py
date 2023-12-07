import os
import json
import socket
import uuid
import random



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
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for user in data_users:
            if (my_info['port'] != user['port'] and my_info['nome'] != user['nome']):
                try:
                    client_socket.sendto(json.dumps(objMsg).encode(), (user['host'], user['port']))
                except Exception as e:
                    print(e)
        return True
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





# Não envia sempre.
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
                        objJson = json.dumps(objFormatado)
                        client_socket.sendto(objJson.encode(), (user['host'], user['port']))
                    print("\n")

        except Exception as e:
            print("Error during sending:", e)
        finally:
            client_socket.close()


def organize_message_dict(dataObj, dict_sync):
    try:
        id_list = dataObj['id_list']

        if id_list in dict_sync:
            dict_sync[id_list].append(dataObj)
        else:
            dict_sync[id_list] = [dataObj]
    except KeyboardInterrupt:
        print("Servidor encerrado pelo usuário.")

def check_full_dict(list_sync):
    completo = True
    for chave, lista_mensagens in list_sync.items():
        tamanho_atual = len(lista_mensagens)
        tamanho_total = lista_mensagens[0].get('size', 0)

        if tamanho_atual != tamanho_total:
            completo = False

    return completo

def extrair_e_ordenar_mensagens(list_sync):
    mensagens_unicas = {}

    for lista_mensagens_usuario in list_sync.values():
        for mensagem in lista_mensagens_usuario:
            mensagem_sem_id_list = {k: v for k, v in mensagem.items() if k != 'id_list'}

            chave = (mensagem_sem_id_list['body']['time'], mensagem_sem_id_list['body']['id'])
            if chave not in mensagens_unicas:
                mensagens_unicas[chave] = mensagem_sem_id_list['body']

    return sorted(mensagens_unicas.values(), key=lambda x: (x['time'], x['id']))


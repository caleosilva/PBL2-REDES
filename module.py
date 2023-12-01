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

# e se ele não receber alguma? Tratar esse caso futuramente
def send_message_list(message_list, user_socket):
    size = len(message_list)
    for objMsg in message_list:
        objFormatado = {'size': size, 'header':'msg-sync', 'body':objMsg}
        user_socket.send((json.dumps(objFormatado)).encode('utf-8'))

# e se ele não receber alguma? Tratar esse caso futuramente
def recv_message_list(user_socket):
    message = user_socket.recv(1024).decode()
    jsonMessage = json.loads(message)

    list_message = [jsonMessage['body']]

    total_size = jsonMessage['size']

    for n in range(total_size - 1):
        jsonMessage = json.loads(user_socket.recv(1024).decode())
        list_message.append(jsonMessage['body'])
    
    return list_message

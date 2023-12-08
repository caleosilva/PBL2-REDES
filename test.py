import random

list_sync = {
    '309587811829': [
        {'id_list': '309587811829', 'size': 3, 'type': 'sync_list_response', 'body': {'time': 1, 'id': '928336c2-827c-4600-8626-f91007431ad7', 'msg': 'opa', 'sender': {'host': '127.0.0.1', 'port': 1111, 'nome': 'jose'}}}, 
        {'id_list': '309587811829', 'size': 3, 'type': 'sync_list_response', 'body': {'time': 2, 'id': 'cb795c7c-f406-4fe1-b350-c403f658baf9', 'msg': 'jose', 'sender': {'host': '127.0.0.1', 'port': 1111, 'nome': 'jose'}}}, 
        {'id_list': '309587811829', 'size': 3, 'type': 'sync_list_response', 'body': {'time': 4, 'id': '357632f4-03a4-4af8-b58a-2131bc1b22ac', 'msg': '123', 'sender': {'host': '127.0.0.1', 'port': 2222, 'nome': 'maria'}}}
        ], 
    '928786384046': [
        {'id_list': '928786384046', 'size': 1, 'type': 'sync_list_response', 'body': {'time': 4, 'id': '357632f4-03a4-4af8-b58a-2131bc1b22ac', 'msg': '123', 'sender': {'host': '127.0.0.1', 'port': 2222, 'nome': 'maria'}}}
        ]
    }


def criptografar(frase):
    mensagem = ""
    for i in frase:
        mensagem += chr (ord(i) + 5)
    return mensagem

def descriptografar(mensagem):
    frase = ""
    for i in mensagem:
        frase += chr (ord(i) - 5)
    return frase


x = criptografar("Meu nome é Caleo")
print(x)

print(descriptografar(x))


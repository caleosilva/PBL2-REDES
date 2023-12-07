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





def extrair_e_ordenar_mensagens(list_sync):
    # Dicionário para garantir mensagens únicas
    mensagens_unicas = {}

    for lista_mensagens_usuario in list_sync.values():
        for mensagem in lista_mensagens_usuario:
            # Remover a chave 'id_list'
            mensagem_sem_id_list = {k: v for k, v in mensagem.items() if k != 'id_list'}

            # Utilizar uma tupla (time, id) como chave para garantir ordenação desejada
            chave = (mensagem_sem_id_list['body']['time'], mensagem_sem_id_list['body']['id'])
            if chave not in mensagens_unicas:
                mensagens_unicas[chave] = mensagem_sem_id_list['body']

    # Ordenar a lista de mensagens pela tupla (time, id)
    lista_mensagens = sorted(mensagens_unicas.values(), key=lambda x: (x['time'], x['id']))

    return lista_mensagens

# lista_mensagens = extrair_e_ordenar_mensagens(list_sync)
# print(lista_mensagens)



def check_full_dict(list_sync):
    completo = True
    for chave, lista_mensagens in list_sync.items():
        tamanho_atual = len(lista_mensagens)
        tamanho_total = lista_mensagens[0].get('size', 0)

        if tamanho_atual != tamanho_total:
            completo = False

    return completo

verificacao = check_full_dict (list_sync)
print(verificacao)
list_sync = {
    15243: [{'id_list': 15243, 'msg': 'oi', 'time': 1, 'id': 'ABC321'}, {'id_list': 15243, 'msg': 'opaa', 'time': 2, 'id': '3333'}],
    98765: [{'id_list': 98765, 'msg': 'opaa', 'time': 2, 'id': '2222'}],
}

def extrair_e_ordenar_mensagens(list_sync):
    # Dicionário para garantir mensagens únicas
    mensagens_unicas = {}

    for lista_mensagens_usuario in list_sync.values():
        for mensagem in lista_mensagens_usuario:
            # Remover a chave 'id_list'
            mensagem_sem_id_list = {k: v for k, v in mensagem.items() if k != 'id_list'}

            # Utilizar uma tupla (time, id) como chave para garantir ordenação desejada
            chave = (mensagem_sem_id_list['time'], mensagem_sem_id_list['id'])
            if chave not in mensagens_unicas:
                mensagens_unicas[chave] = mensagem_sem_id_list

    # Ordenar a lista de mensagens pela tupla (time, id)
    lista_mensagens = sorted(mensagens_unicas.values(), key=lambda x: (x['time'], x['id']))

    return lista_mensagens

# Chamando a função para extrair e ordenar mensagens únicas, removendo 'id_list'
lista_mensagens = extrair_e_ordenar_mensagens(list_sync)

# Exibindo o resultado
print(lista_mensagens)

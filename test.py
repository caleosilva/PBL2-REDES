HOST_LISTEN = "10.0.0.103"


mi_redes = [
    {'index': 1, 'id': '0d623e1a-1e0a-4c72-9455-e9268f880768', 'msg': 'Alguem online?', 'sender': {"host": HOST_LISTEN, "port": 1111, "nome": "jose"}},
    {'index': 2, 'id': '07908719-c648-4e2e-ba1d-b176a897db78', 'msg': 'Aloo?', 'sender': {"host": HOST_LISTEN, "port": 1111, "nome": "jose"}},
    {'index': 3, 'id': 'e28f3b19-386e-43b3-b030-22ef0269fb1e', 'msg': 'Oii, to aqui', 'sender':     {"host": HOST_LISTEN, "port": 2222, "nome": "maria"}}
]



def get_my_latest_id(list_messages):
    last_id = False

    if (len(list_messages) > 0):
        last_id = list_messages[-1]['index']
            
    return last_id

x = get_my_latest_id(mi_redes)
print(x)
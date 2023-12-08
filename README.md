<div align="center">
  <h1>
      Relatório do problema 2: ZapsZap
  </h1>

  <h3>
    Georgenes Caleo Silva Pinheiro
  </h3>

  <p>
    Engenharia de Computação – Universidade Estadual de Feira de Santana (UEFS)
    Av. Transnordestina, s/n, Novo Horizonte
    Feira de Santana – BA, Brasil – 44036-900
  </p>

  <center>caleosilva75@gmail.com</center>

</div>

# 1. Introdução

Nos últimos anos, a crescente importância dos aplicativos de mensagens no ambiente corporativo tem se destacado como uma ferramenta fundamental para aprimorar a comunicação entre indivíduos e equipes. No entanto, depender de serviços de terceiros nem sempre é a opção mais ideal, especialmente quando requisitos cruciais de arquitetura e segurança não são plenamente atendidos.

Nesse cenário, uma startup optou por investir no desenvolvimento de uma nova solução de mensagens instantâneas direcionada ao mercado corporativo. Essa inovação baseia-se no modelo peer-to-peer (P2P), visando oferecer uma abordagem descentralizada, eliminando a necessidade de um servidor central. Além disso, a ênfase está na segurança da comunicação, com a implementação de mensagens criptografadas.

A concretização desse sistema ocorreu por meio da linguagem de programação Python, versão 3.11, e suas bibliotecas internas, incluindo threading, socket, time e queue. A decisão de desenvolver e testar o produto utilizando containers Docker reflete o comprometimento com a eficiência e a consistência. Para garantir uma comunicação eficaz, a implementação foi construída sobre a arquitetura de rede baseada em UDP. Esse conjunto de escolhas tecnológicas e ferramentas resultou na criação de um sistema robusto e eficiente, capaz de atender plenamente às demandas específicas da startup.

# 2. Metodologia

bla bla bla

# 3. Resultados

bla bla bla

# 4. Conclusão

bla bla bla

# Referências

Python threading module: Disponível em: https://docs.python.org/3/library/threading.html. Acesso em: 23 de ago. de 2023

HUNT, John; HUNT, John. Sockets in Python. Advanced Guide to Python 3 Programming, p. 457-470, 2019.



----------------------------------------------

6 - threads:
- ask_sync_clock_and_list
- receive_dict_sync
- server
- handle_request
- write_prepare_message
- sync_active

Envio dos pacotes no formato:
type: n diferentes 
{...}

Sincronização:
Relógio de lamport
A cada 10 seg as listas são trocadas

Login
Como é feito?

Criptografia:
Simples, falhas

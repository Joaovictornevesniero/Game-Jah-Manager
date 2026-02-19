import os
import psutil
import time
import difflib
from repositorio import salvar_jogo_sql


def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def cadastrar_jogo():
    """
    Decide qual modo de cadastro usar.
    """

    limpar_terminal()
    print('=== CADASTRAR JOGO ===\n')

    nome = input('Nome do jogo: ').strip()
    if not nome:
        print('Nome inválido.')
        return

    resposta = input('O jogo já está aberto? (s/n): ').strip().lower()

    if resposta == 's':
        cadastrar_jogo_aberto(nome)
    else:
        cadastrar_jogo_fechado(nome)


def cadastrar_jogo_aberto(nome):
    """
    Lista processos parecidos com o nome digitado.
    """

    ignorar = {
        'svchost.exe',
        'System',
        'Registry',
        'Idle',
        'RuntimeBroker.exe',
        'SearchIndexer.exe',
        'ShellExperienceHost.exe'
    }

    processos = set()

    for p in psutil.process_iter(['name']):
        try:
            nome_proc = p.info['name']
            if nome_proc and nome_proc not in ignorar:
                processos.add(nome_proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # remove .exe para comparar melhor
    processos_sem_ext = [p.replace('.exe', '') for p in processos]
    nome_base = nome.lower()

    parecidos = difflib.get_close_matches(
        nome_base,
        [p.lower() for p in processos_sem_ext],
        n=10,
        cutoff=0.2
    )

    if not parecidos:
        print('\nNenhum processo parecido encontrado.')
        return

    print('\n=== PROCESSOS PARECIDOS ===\n')

    lista_final = []
    for i, proc in enumerate(parecidos, 1):
        nome_real = proc + '.exe'
        print(f'{i} - {nome_real}')
        lista_final.append(nome_real)

    print('0 - Cancelar')

    try:
        escolha = int(input('\nEscolha: '))
        if escolha == 0:
            return
        processo_escolhido = lista_final[escolha - 1]
    except:
        print('Escolha inválida.')
        return

    salvar_jogo_sql(nome, processo_escolhido)
    print(f'\nJogo cadastrado: {nome} ({processo_escolhido})')


def cadastrar_jogo_fechado(nome):
    """
    Compara processos antes e depois de abrir o jogo.
    """

    ignorar = {
        'svchost.exe',
        'System',
        'Registry',
        'Idle',
        'RuntimeBroker.exe',
        'SearchIndexer.exe',
        'ShellExperienceHost.exe'
    }

    antes = set()

    for p in psutil.process_iter(['name']):
        try:
            nome_proc = p.info['name']
            if nome_proc and nome_proc not in ignorar:
                antes.add(nome_proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    print('\nAbra o jogo agora.')
    input('Pressione ENTER após o jogo abrir...')
    time.sleep(2)

    depois = set()

    for p in psutil.process_iter(['name']):
        try:
            nome_proc = p.info['name']
            if nome_proc and nome_proc not in ignorar:
                depois.add(nome_proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    novos = list(depois - antes)

    if not novos:
        print('\nNenhum processo novo detectado.')
        return

    print('\n=== PROCESSOS NOVOS DETECTADOS ===\n')

    for i, proc in enumerate(novos, 1):
        print(f'{i} - {proc}')

    print('0 - Cancelar')

    try:
        escolha = int(input('\nEscolha: '))
        if escolha == 0:
            return
        processo_escolhido = novos[escolha - 1]
    except:
        print('Escolha inválida.')
        return

    salvar_jogo_sql(nome, processo_escolhido)
    print(f'\nJogo cadastrado: {nome} ({processo_escolhido})')

#Arquivo de cadastro, serve para cadastrar os jogos na tabela jogos.
import os
import psutil
import time
import difflib
from repositorio import salvar_jogo_sql
from utils import limpar_terminal, validar_ate, pausa

def menu_cadastro_auto_manual():
    print('=== CADASTRAR JOGO ===\n')
    print('1- Cadastro Semi-Automático')
    print('2- Cadastro Manual')
    print('0- Voltar menu')


def cadastrar_jogo():
    """
    Decide qual modo de cadastro usar.
    """

    limpar_terminal()
    menu_cadastro_auto_manual()
    opcao= validar_ate(2)
    if opcao == 1:
        nome = input('Nome do jogo: ').strip()
        if not nome:
            print('Nome inválido.')
            return

        resposta = input('O jogo já está aberto? (s/n): ').strip().lower()

        if resposta == 's':
            cadastrar_jogo_aberto(nome)
        else:
            cadastrar_jogo_fechado(nome)
    elif opcao == 2:
        cadastrar_jogo_manual()
    

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
    pausa()

def cadastrar_jogo_fechado(nome):
    """
    Compara processos antes e depois de abrir o jogo.
    Mostra a diferença e permite escolher qual cadastrar.
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

    # -------------------------
    # PROCESSOS ANTES
    # -------------------------
    antes = set()

    for p in psutil.process_iter(['name']):
        try:
            nome_proc = p.info['name']
            if nome_proc and nome_proc not in ignorar:
                antes.add(nome_proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    print('\nAbra o jogo agora.')
    input('\nPressione ENTER após o jogo abrir...')
    time.sleep(2)

    # -------------------------
    # PROCESSOS DEPOIS
    # -------------------------
    depois = set()

    for p in psutil.process_iter(['name']):
        try:
            nome_proc = p.info['name']
            if nome_proc and nome_proc not in ignorar:
                depois.add(nome_proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # -------------------------
    # DIFERENÇA
    # -------------------------
    novos = sorted(list(depois - antes))

    print('\n=== DIFERENÇA DE PROCESSOS ===\n')
    print(f'Antes: {len(antes)} processos')
    print(f'Depois: {len(depois)} processos')
    print(f'Novos detectados: {len(novos)}\n')

    if not novos:
        print('Nenhum processo novo detectado.')
        pausa()
        return

    for i, proc in enumerate(novos, 1):
        print(f'{i} - {proc}')

    print('0 - Cancelar')

    # -------------------------
    # LOOP DE VALIDAÇÃO
    # -------------------------
    while True:
        escolha = validar_ate(len(novos))

        # Se validar_ate não retornou nada
        if escolha is None:
            continue

        # Se estiver fora do intervalo por algum motivo
        if not (0 <= escolha <= len(novos)):
            continue

        break

    if escolha == 0:
        print('\nCadastro cancelado.')
        pausa()
        return

    processo_escolhido = novos[escolha - 1]

    # SALVAR
    salvar_jogo_sql(nome, processo_escolhido)

    print(f'\nJogo cadastrado: {nome} ({processo_escolhido})')
    pausa()

def cadastrar_jogo_manual():
    """
    Permite cadastrar um jogo informando manualmente
    o nome e o processo executável.
    """

    limpar_terminal()
    print('=== CADASTRO MANUAL DE JOGO ===\n')

    nome = input('Nome do jogo: ').strip()
    if not nome:
        print('Nome inválido.')
        return

    nome_processo = input('Nome do processo (ex: Minecraft.exe): ').strip().lower()
    if not nome_processo:
        print('Processo inválido.')
        return

    # Garante que termine com .exe
    if not nome_processo.endswith('.exe'):
        nome_processo += '.exe'

    salvar_jogo_sql(nome, nome_processo)

    print(f'\nJogo cadastrado manualmente: {nome} ({nome_processo})')
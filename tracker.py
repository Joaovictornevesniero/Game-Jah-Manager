import psutil
import json
import os
import time
import msvcrt
from datetime import datetime

#Banco de dados
JOGOS_DB = 'jogos.json'
HIST_DB = 'gameplay.json'


def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def processo_rodando(nome_processo):
    '''
    Verifica se um processo específico está rodando.

    Args:
        nome_processo (str): Nome exato do processo (ex: eldenring.exe)

    Returns:
        bool: True se estiver rodando, False se não
    '''
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == nome_processo:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False


def salvar_historico(jogo, inicio, fim, tempo):
    '''
    Salva uma sessão de gameplay no histórico.
    '''
    historico = []

    if os.path.exists(HIST_DB):
        with open(HIST_DB, encoding='utf-8') as f:
            historico = json.load(f)

    historico.append({
        'jogo': jogo,
        'inicio': inicio,
        'fim': fim,
        'tempo': tempo
    })

    with open(HIST_DB, 'w', encoding='utf-8') as f:
        json.dump(historico, f, indent=4, ensure_ascii=False)


def monitorar():
    '''
    Monitora o tempo de jogo baseado no processo cadastrado.
    '''
    if not os.path.exists(JOGOS_DB):
        print('Nenhum jogo cadastrado.')
        return

    with open(JOGOS_DB, encoding='utf-8') as f:
        jogos = json.load(f)

    if not jogos:
        print('Nenhum jogo cadastrado.')
        return

    nomes = list(jogos.keys())

    limpar_terminal()
    print('=== ESCOLHER JOGO ===\n')

    for i, nome in enumerate(nomes, 1):
        print(f'{i} - {nome}')
    print('0 - Cancelar')

    try:
        escolha = int(input('\nEscolha: '))
        if escolha == 0:
            return
        nome_jogo = nomes[escolha - 1]
    except:
        return

    processo = jogos[nome_jogo]

    limpar_terminal()
    print(f'Monitorando: {nome_jogo}')
    print('Pressione [Q] para encerrar o monitoramento.\n')

    inicio = None
    inicio_str = None

    while True:
        #Encerrar manual
        if msvcrt.kbhit():
            tecla = msvcrt.getch().decode('utf-8').lower()
            if tecla == 'q' and inicio:
                fim = datetime.now()
                fim_str = fim.strftime("%d/%m/%Y %H:%M:%S")
                total = str(fim - inicio).split('.')[0]
                salvar_historico(nome_jogo, inicio_str, fim_str, total)
                print(f'\nMonitoramento encerrado manualmente ({total})')
                return

        ativo = processo_rodando(processo)

        #Jogo aberto
        if ativo and not inicio:
            inicio = datetime.now()
            inicio_str = inicio.strftime("%d/%m/%Y %H:%M:%S")

        if ativo and inicio:
            tempo = datetime.now() - inicio
            print(f'Tempo jogando: {str(tempo).split('.')[0]}', end='\r')

        #Jogo fechado
        if not ativo and inicio:
            fim = datetime.now()
            fim_str = fim.strftime("%d/%m/%Y %H:%M:%S")
            total = str(fim - inicio).split('.')[0]
            salvar_historico(nome_jogo, inicio_str, fim_str, total)
            print(f'\nSessão salva automaticamente ({total})')
            return

        time.sleep(1)


def ver_historico():
    limpar_terminal()
    print('=== HISTÓRICO DE GAMEPLAY ===\n')

    if not os.path.exists(HIST_DB):
        print('Nenhum histórico encontrado.')
        return

    with open(HIST_DB, encoding="utf-8") as f:
        historico = json.load(f)

    if not historico:
        print('Histórico vazio.')
        return

    for i, h in enumerate(historico, 1):
        print(f"{i}. {h['jogo']}")
        print(f"   Início: {h['inicio']}")
        print(f"   Fim:    {h['fim']}")
        print(f"   Tempo:  {h['tempo']}\n")

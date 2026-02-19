import psutil
import os
import time
import msvcrt
from datetime import datetime
from repositorio import listar_jogos, salvar_sessao, listar_sessoes

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def processo_rodando(nome_processo):
    nome_processo = nome_processo.lower().strip()

    for proc in psutil.process_iter(['name']):
        try:
            nome_atual = proc.info['name']

            if nome_atual and nome_atual.lower().strip() == nome_processo:
                return True

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return False



def ver_historico():
    limpar_terminal()
    print('=== HISTÓRICO DE GAMEPLAY ===\n')

    sessoes = listar_sessoes()

    if not sessoes:
        print('Histórico vazio.')
        return

    for i, s in enumerate(sessoes, 1):
        print(f"{i}. {s[1]}")
        print(f"   Início: {s[2]}")
        print(f"   Fim:    {s[3]}")
        print(f"   Tempo:  {s[4]} segundos\n")


def monitorar():
    '''
    Monitora o tempo de jogo baseado no processo cadastrado.
    '''

    jogos = listar_jogos()

    if not jogos:
        print('Nenhum jogo cadastrado.')
        return

    limpar_terminal()
    print('=== ESCOLHER JOGO ===\n')

    for i, jogo in enumerate(jogos, 1):
        print(f'{i} - {jogo[1]}')
    print('0 - Cancelar')

    try:
        escolha = int(input('\nEscolha: '))
        if escolha == 0:
            return
        jogo_id, nome_jogo, processo = jogos[escolha - 1]
    except:
        return

    limpar_terminal()
    print(f'Monitorando: {nome_jogo}')
    print('Pressione [Q] para encerrar o monitoramento.\n')

    inicio = None
    inicio_str = None

    while True:

        # =========================
        # ENCERRAR MANUAL (Q)
        # =========================
        if msvcrt.kbhit():
            try:
                tecla = msvcrt.getch().decode(errors='ignore').lower()
                if tecla == 'q' and inicio:
                    fim = datetime.now()
                    fim_str = fim.strftime("%d/%m/%Y %H:%M:%S")
                    duracao_segundos = int((fim - inicio).total_seconds())

                    salvar_sessao(jogo_id, inicio_str, fim_str, duracao_segundos)

                    print(f'\nMonitoramento encerrado manualmente ({duracao_segundos} segundos)')
                    return
            except:
                pass

        ativo = processo_rodando(processo)

        # =========================
        # JOGO ABERTO
        # =========================
        if ativo and not inicio:
            inicio = datetime.now()
            inicio_str = inicio.strftime("%d/%m/%Y %H:%M:%S")

        if ativo and inicio:
            tempo = datetime.now() - inicio
            tempo_formatado = str(tempo).split('.')[0]
            print(f'Tempo jogando: {tempo_formatado}', end='\r', flush=True)

        # =========================
        # JOGO FECHADO
        # =========================
        if not ativo and inicio:
            fim = datetime.now()
            fim_str = fim.strftime("%d/%m/%Y %H:%M:%S")
            duracao_segundos = int((fim - inicio).total_seconds())

            salvar_sessao(jogo_id, inicio_str, fim_str, duracao_segundos)

            print(f'\nSessão salva automaticamente ({duracao_segundos} segundos)')
            return

        time.sleep(1)

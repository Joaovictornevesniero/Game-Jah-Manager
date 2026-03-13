#Arquivo de cadastro e monitoramento, serve para monitorar os jogos e salvar na tabela sessões.
import psutil
import os
import time
import msvcrt
from datetime import datetime
from utils import limpar_terminal, validar_ate, pausa
from repositorio import listar_jogos, salvar_sessao, listar_sessoes, relatorio_total_por_jogo

#Monitoramento
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


def monitorar():
    jogos = listar_jogos()

    if not jogos:
        print('Nenhum jogo cadastrado.')
        pausa('Pressione ENTER para voltar ao menu...')
        return
    #Inicio do bloco do menu
    limpar_terminal()
    print('=== ESCOLHER JOGO ===\n')

    for i, jogo in enumerate(jogos, 1):
        print(f'{i} - {jogo[1]}')
    print('0 - Cancelar')

    escolha = validar_ate(len(jogos))

    if escolha == 0:
        return
    #fim do bloco do menu
    jogo_id, nome_jogo, processo = jogos[escolha - 1]

    limpar_terminal()
    print(f'Monitorando: {nome_jogo}')
    print('Pressione [Q] para encerrar o monitoramento.\n')

    inicio = None
    inicio_str = None

    while True:
        #Inicio do bloco de Verificar se a tecla Q for pressionada, funciona só no windows.
        if msvcrt.kbhit(): #Se alguma tecla for pressionada
            try:
                tecla = msvcrt.getch().decode(errors='ignore').lower() #Formatação pro Q
                if tecla == 'q' and inicio:
                    fim = datetime.now()
                    fim_str = fim.strftime("%d/%m/%Y %H:%M:%S")
                    duracao_segundos = int((fim - inicio).total_seconds())

                    salvar_sessao(jogo_id, inicio_str, fim_str, duracao_segundos)

                    print(f'\nMonitoramento encerrado manualmente ({duracao_segundos} segundos)')
                    pausa('Pressione ENTER para voltar ao menu...')
                    return
            except:
                pass
        #Fim do bloco de Verificar se a tecla Q for pressionada.

        ativo = processo_rodando(processo)

        if ativo and not inicio: #Se o processo está ativo e contador não tinha sido iniciado, significa que o jogo foi aberto, registra a hora e começa a contagem.
            inicio = datetime.now()
            inicio_str = inicio.strftime("%d/%m/%Y %H:%M:%S")

        if ativo and inicio:  #Se o processo está ativo e contador iniciou, significa o jogo está rodando, apenas atualiza o tempo real.
            tempo = datetime.now() - inicio
            tempo_formatado = str(tempo).split('.')[0]
            print(f'Tempo jogando: {tempo_formatado}', end='\r', flush=True)

        if not ativo and inicio: #Se o processo não está ativo e o contator iniciou, significa o jogo foi fechado.
            fim = datetime.now()
            fim_str = fim.strftime("%d/%m/%Y %H:%M:%S")
            duracao_segundos = int((fim - inicio).total_seconds())

            salvar_sessao(jogo_id, inicio_str, fim_str, duracao_segundos)

            print(f'\nSessão salva automaticamente ({duracao_segundos} segundos)')
            pausa('Pressione ENTER para voltar ao menu...')
            return

        time.sleep(1)

#Históricos
def formatar_tempo(total_segundos):
    horas = total_segundos // 3600
    minutos = (total_segundos % 3600) // 60
    segundos = total_segundos % 60

    return f"{horas}h {minutos}m {segundos}s"


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
        tempo = formatar_tempo(s[4])
        print(f"   Tempo:  {tempo}\n")
    pausa('Pressione ENTER para voltar ao menu...')


def gerar_relatorio():
    limpar_terminal()
    print('=== RELATÓRIO TOTAL DE GAMEPLAY ===\n')

    dados = relatorio_total_por_jogo()

    if not dados:
        print('Nenhuma sessão registrada.')
        pausa('Pressione ENTER para voltar ao menu...')
        return

    for i, (nome, total_segundos) in enumerate(dados, 1):
        if total_segundos is None:
            total_segundos = 0

        tempo_formatado = formatar_tempo(total_segundos)

        print(f"{i}. {nome}")
        print(f"   Total jogado: {tempo_formatado}\n")

    pausa('Pressione ENTER para voltar ao menu...')
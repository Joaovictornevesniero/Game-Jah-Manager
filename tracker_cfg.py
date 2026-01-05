import json
import os
import psutil
import time
import difflib

#Banco de dados dos jogos cadastrados
JOGOS_DB = 'jogos.json'


def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def cadastrar_jogo():
    """
    Cadastro de um novo jogo.

    Fluxo:
    - Usuário informa o nome do jogo
    - Abre o jogo manualmente
    - O script tenta detectar qual processo surgiu
    - Caso não consiga, permite escolha manual
    - Salva o nome do jogo + nome do processo
    """
    limpar_terminal()
    print('=== CADASTRAR JOGO ===\n')

    nome = input('Nome do jogo: ').strip()
    if not nome:
        print('Nome inválido.')
        return

    print('\nAbra o jogo agora.')
    input('Pressione ENTER para continuar...')

    antes = {
        p.info['name']
        for p in psutil.process_iter(['name'])
        if p.info['name']
    }

    time.sleep(1)

    depois = {
        p.info['name']
        for p in psutil.process_iter(['name'])
        if p.info['name']
    }

    novos = list(depois - antes)

    if len(novos) == 1:
        processo = novos[0]

    else:
        print('\nTentando detectar processo parecido...\n')

        similares = difflib.get_close_matches(
            nome,
            list(depois),
            n=5,
            cutoff=0.3
        )

        if not similares:
            print('Não foi possível detectar o processo.\n')
            print('0 - Voltar ao menu')
            print('1 - Ver todos os processos')

            escolha = input("\nEscolha: ").strip()

            if escolha == '0':
                return

            elif escolha == '1':
                todos_processos = sorted({
                    p.info['name']
                    for p in psutil.process_iter(['name'])
                    if p.info['name']
                })

                limpar_terminal()
                print('=== PROCESSOS ATIVOS ===\n')

                for i, p in enumerate(todos_processos, 1):
                    print(f"{i} - {p}")

                try:
                    indice = int(input('\nEscolha o processo: ')) - 1
                    processo = todos_processos[indice]
                except:
                    print('Escolha inválida.')
                    return

            else:
                print('Opção inválida.')
                return

        else:
            for i, p in enumerate(similares, 1):
                print(f"{i} - {p}")

            try:
                processo = similares[int(input('\nEscolha: ')) - 1]
            except:
                print('Escolha inválida.')
                return

    jogos = {}
    if os.path.exists(JOGOS_DB):
        with open(JOGOS_DB, encoding='utf-8') as f:
            jogos = json.load(f)

    jogos[nome] = processo

    with open(JOGOS_DB, 'w', encoding='utf-8') as f:
        json.dump(jogos, f, indent=4, ensure_ascii=False)

    print(f'\nJogo cadastrado: {nome} ({processo})')

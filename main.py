#Arquivo principal, roda o programa e contém todas as funções relacionadas a menus.
#Bibliotecas/Módulos.
import os
import sys
import tracker
import tracker_cfg
from time import sleep
from database import criar_tabelas
from repositorio import listar_jogos, atualizar_jogo, remover_jogo
from utils import limpar_terminal, validar_ate, pausa

#Funções
def menu():
    limpar_terminal()
    print('=== GAME TIME MANAGER TRACKER ===\n')
    print('1 - Monitorar jogo')
    print('2 - Cadastro de jogos')
    print('3 - Tempo de gameplay')
    print('0 - Sair')


def menu_cadastro():
    limpar_terminal()
    print('=== CADASTRO/ATUALIZAÇÃO DE JOGOS ===\n')
    print('1 - Cadastrar novo jogo')
    print('2 - Listar jogos cadastrados')
    print('3 - Alterar algum jogo manualmente')
    print('4 - Remover algum jogo')
    print('0 - Sair')


def menu_run():
    limpar_terminal()
    print('=== HISTÓRICO DE RUNS ===\n')
    print('1 - Relatório de runs individuais')
    print('2 - Relatório de runs completo')
    print('0 - Sair')


def listar_jogos_menu():
    limpar_terminal()
    print('=== JOGOS CADASTRADOS ===\n')
    jogos = listar_jogos()
    if not jogos:
        print('Nenhum jogo cadastrado.')
        return
    for jogo in jogos:
        print(f'ID: {jogo[0]} | {jogo[1]} | Processo: {jogo[2]}')


def atualizar_jogo_pelo_menu():
    listar_jogos_menu()
    try:
        id_jogo = int(input('\nID do jogo para atualizar: '))
        novo_nome = input('Novo nome: ').strip()
        novo_processo = input('Novo processo: ').strip()
    except:
        print('Entrada inválida.')
        return
    atualizar_jogo(id_jogo, novo_nome, novo_processo)
    input('\nJogo atualizado.')


def remover_jogo_pelo_menu():
    listar_jogos_menu()
    try:
        id_jogo = int(input('\nID do jogo para remover: '))
    except:
        print('\nEntrada inválida.')
        return
    remover_jogo(id_jogo)
    input('\nJogo removido.')


def main():
    while True:
        limpar_terminal()
        menu()
        opcao= validar_ate(3)

        if opcao == 0:
            print('\nSaindo...')
            sleep(1)
            limpar_terminal()
            sys.exit()

        elif opcao == 1:
            tracker.monitorar()

        elif opcao == 2:
            menu_cadastro()
            opcao= validar_ate(4)
            if opcao == 1:
                tracker_cfg.cadastrar_jogo()
            elif opcao == 2:
                listar_jogos_menu()
            elif opcao == 3:
                atualizar_jogo_pelo_menu()
            elif opcao == 4:
                remover_jogo_pelo_menu()

        elif opcao == 3:
            menu_run()
            opcao= validar_ate(2)
            if opcao == 1:
                tracker.ver_historico()
            elif opcao == 2:
                tracker.gerar_relatorio()

#Programa principal
if __name__ == '__main__':
    criar_tabelas()
    main()
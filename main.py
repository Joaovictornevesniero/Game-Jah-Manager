#Bibliotecas/Módulos.
import os
import sys
import tracker
import tracker_cfg

#Funções
def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    input("\nPressione ENTER para continuar...")


def menu():
    """
    Mostra o menu principal do programa.
    """
    print('=== GAME TIME MANEGER TRACKER ===\n')
    print('1 - Monitorar jogo')
    print('2 - Cadastrar novo jogo')
    print('3 - Ver histórico')
    print('0 - Sair')


def main():
    """
    Loop principal do programa.
    Controla o menu e redireciona para as funções corretas.
    """
    while True:
        limpar_terminal()
        menu()

        try:
            opcao = int(input('\nEscolha: '))
        except ValueError:
            continue

        if opcao == 0:
            limpar_terminal()
            print('Saindo...')
            sys.exit()

        elif opcao == 1:
            tracker.monitorar()

        elif opcao == 2:
            tracker_cfg.cadastrar_jogo()

        elif opcao == 3:
            tracker.ver_historico()

        pausar()

#Programa principal.
if __name__ == '__main__':
    main()


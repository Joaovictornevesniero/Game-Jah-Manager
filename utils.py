import os


def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def validar_ate(max_opcao):
        try:
            opcao = int(input('\nEscolha: '))
            
            if 0 <= opcao <= max_opcao:
                return opcao
            else:
                input(f"\nDigite um número entre 0 e {max_opcao}...")
        except ValueError:
            input("\nDigite apenas números...")


def pausa(a=' '):
     input(f'{a}')
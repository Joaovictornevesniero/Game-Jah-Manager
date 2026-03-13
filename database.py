#Arquivo de criação de tabelas, serve apenas para criar as tabelas no banco de dados.
import sqlite3

NOME_BANCO = "game_jah.db"


def obter_conexao():
    return sqlite3.connect(NOME_BANCO)


def criar_tabelas():
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jogos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        nome_processo TEXT NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jogo_id INTEGER,
        inicio TEXT NOT NULL,
        fim TEXT,
        duracao_segundos INTEGER,
        FOREIGN KEY (jogo_id) REFERENCES jogos(id)
    )
    """)

    conexao.commit()
    conexao.close()
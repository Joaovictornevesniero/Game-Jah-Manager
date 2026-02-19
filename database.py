import sqlite3

NOME_BANCO = "game_jah.db"


def obter_conexao():
    """
    Retorna uma conexão com o banco SQLite.
    """
    return sqlite3.connect(NOME_BANCO)


def criar_tabelas():
    """
    Cria as tabelas necessárias caso não existam.
    """
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jogos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        nome_processo TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jogo_id INTEGER,
        inicio TEXT NOT NULL,
        fim TEXT NOT NULL,
        duracao_segundos INTEGER NOT NULL,
        FOREIGN KEY (jogo_id) REFERENCES jogos(id)
    )
    """)

    conexao.commit()
    conexao.close()

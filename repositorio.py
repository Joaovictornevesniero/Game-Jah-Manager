from database import obter_conexao

# =========================
# JOGOS
# =========================

def salvar_jogo_sql(nome, nome_processo):
    """
    Salva um novo jogo no banco de dados.
    """
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO jogos (nome, nome_processo) VALUES (?, ?)",
        (nome, nome_processo)
    )

    conexao.commit()
    conexao.close()


def listar_jogos():
    """
    Retorna todos os jogos cadastrados.
    """
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("SELECT id, nome, nome_processo FROM jogos")
    jogos = cursor.fetchall()

    conexao.close()
    return jogos


def atualizar_jogo(id_jogo, novo_nome, novo_processo):
    """
    Atualiza os dados de um jogo existente.
    """
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE jogos
        SET nome = ?, nome_processo = ?
        WHERE id = ?
    """, (novo_nome, novo_processo, id_jogo))

    conexao.commit()
    conexao.close()


def remover_jogo(id_jogo):
    """
    Remove um jogo do banco de dados.
    """
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM jogos WHERE id = ?", (id_jogo,))

    conexao.commit()
    conexao.close()


# =========================
# SESSÕES
# =========================

def salvar_sessao(jogo_id, inicio, fim, duracao_segundos):
    """
    Salva uma sessão de gameplay no banco.
    """
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO sessoes (jogo_id, inicio, fim, duracao_segundos)
        VALUES (?, ?, ?, ?)
    """, (jogo_id, inicio, fim, duracao_segundos))

    conexao.commit()
    conexao.close()


def listar_sessoes():
    """
    Retorna todas as sessões salvas, ordenadas da mais recente para a mais antiga.
    """
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT s.id, j.nome, s.inicio, s.fim, s.duracao_segundos
        FROM sessoes s
        JOIN jogos j ON s.jogo_id = j.id
        ORDER BY s.id DESC
    """)

    sessoes = cursor.fetchall()
    conexao.close()
    return sessoes

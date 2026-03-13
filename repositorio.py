#Arquivo de conexão, serve para salvar, buscar, atualizar ou remover informações do banco de dados, não deve ter nenhum input.
from database import obter_conexao

#Controle da tabela jogos
def salvar_jogo_sql(nome, nome_processo):
    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            "INSERT INTO jogos (nome, nome_processo) VALUES (?, ?)",
            (nome, nome_processo.lower())
        )
        conexao.commit()
        print("Jogo cadastrado com sucesso.")
    except Exception as e:
        print("Erro ao cadastrar jogo:", e)
    finally:
        conexao.close()


def listar_jogos():
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("SELECT id, nome, nome_processo FROM jogos")
    jogos = cursor.fetchall()

    conexao.close()
    return jogos


def atualizar_jogo(id_jogo, novo_nome, novo_processo):
    conexao = obter_conexao()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE jogos
            SET nome = ?, nome_processo = ?
            WHERE id = ?
        """, (novo_nome, novo_processo.lower(), id_jogo))

        conexao.commit()
        print("Jogo atualizado com sucesso.")
    except Exception as e:
        print("Erro ao atualizar jogo:", e)
    finally:
        conexao.close()


def remover_jogo(id_jogo):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM jogos WHERE id = ?", (id_jogo,))
    conexao.commit()
    conexao.close()
    print("Jogo removido com sucesso.")

#Controle da tabela jogos sessões
def salvar_sessao(jogo_id, inicio, fim=None, duracao_segundos=None):
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO sessoes (jogo_id, inicio, fim, duracao_segundos)
        VALUES (?, ?, ?, ?)
    """, (jogo_id, inicio, fim, duracao_segundos))

    conexao.commit()
    conexao.close()


def listar_sessoes():
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


def relatorio_total_por_jogo():
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT j.nome, SUM(s.duracao_segundos) as total_segundos
        FROM sessoes s
        JOIN jogos j ON s.jogo_id = j.id
        GROUP BY j.nome
        ORDER BY total_segundos DESC
    """)

    dados = cursor.fetchall()
    conexao.close()
    return dados
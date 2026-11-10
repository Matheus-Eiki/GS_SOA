
from app.database.connection import conectar


def consultar(sql, parametros=None, unico=False):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(sql, parametros or {})

        colunas = [
            coluna[0].lower()
            for coluna in cursor.description
        ]

        if unico:
            resultado = cursor.fetchone()

            if resultado is None:
                return None

            return dict(zip(colunas, resultado))

        resultados = cursor.fetchall()

        return [
            dict(zip(colunas, linha))
            for linha in resultados
        ]

    finally:
        cursor.close()
        conexao.close()


def executar(sql, parametros=None):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(sql, parametros or {})
        quantidade = cursor.rowcount
        conexao.commit()

        return quantidade

    except Exception:
        conexao.rollback()
        raise

    finally:
        cursor.close()
        conexao.close()


def inserir(sql, parametros=None):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        novo_id = cursor.var(int)

        dados = parametros.copy() if parametros else {}
        dados["id_novo"] = novo_id

        cursor.execute(sql, dados)

        conexao.commit()

        valor_id = novo_id.getvalue()

        # Algumas configurações retornam o ID dentro de uma lista.
        if isinstance(valor_id, (list, tuple)):
            valor_id = valor_id[0] if valor_id else None

        if valor_id is None:
            raise Exception("O Oracle não retornou o ID do registro.")

        return int(valor_id)

    except Exception:
        conexao.rollback()
        raise

    finally:
        cursor.close()
        conexao.close()

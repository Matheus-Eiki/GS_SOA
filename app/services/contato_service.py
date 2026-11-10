
from app.services.db_helper import consultar, executar, inserir


def listar_contatos():
    sql = """
        SELECT *
        FROM CONTATOS_EMERGENCIA
        ORDER BY ID
    """
    return consultar(sql)


def buscar_contato(contato_id: int):
    sql = """
        SELECT *
        FROM CONTATOS_EMERGENCIA
        WHERE ID = :contato_id
    """
    return consultar(sql, {"contato_id": contato_id}, unico=True)


def listar_contatos_usuario(usuario_id: int):
    sql = """
        SELECT *
        FROM CONTATOS_EMERGENCIA
        WHERE USUARIO_ID = :usuario_id
        ORDER BY ID
    """
    return consultar(sql, {"usuario_id": usuario_id})


def criar_contato(dados):
    contato = dados.model_dump()

    sql = """
        INSERT INTO CONTATOS_EMERGENCIA (
            USUARIO_ID,
            NOME,
            PARENTESCO,
            TELEFONE,
            EMAIL,
            PRINCIPAL
        )
        VALUES (
            :usuario_id,
            :nome,
            :parentesco,
            :telefone,
            :email,
            :principal
        )
        RETURNING ID INTO :id_novo
    """

    novo_id = inserir(sql, contato)

    resultado = buscar_contato(novo_id)

    if resultado is None:
        raise Exception("Não foi possível recuperar o contato cadastrado.")

    return resultado


def atualizar_contato(contato_id: int, dados):
    contato = buscar_contato(contato_id)

    if contato is None:
        return None

    dados_atualizados = dados.model_dump(
        exclude_unset=True
    )

    campos_permitidos = {
        "nome": "NOME",
        "parentesco": "PARENTESCO",
        "telefone": "TELEFONE",
        "email": "EMAIL",
        "principal": "PRINCIPAL"
    }

    partes_sql = []
    parametros = {"contato_id": contato_id}

    for campo, valor in dados_atualizados.items():
        if campo in campos_permitidos:
            coluna = campos_permitidos[campo]
            parametro = campo

            partes_sql.append(f"{coluna} = :{parametro}")
            parametros[parametro] = valor

    if not partes_sql:
        return contato

    sql = f"""
        UPDATE CONTATOS_EMERGENCIA
        SET {", ".join(partes_sql)}
        WHERE ID = :contato_id
    """

    executar(sql, parametros)

    return buscar_contato(contato_id)


def excluir_contato(contato_id: int):
    contato = buscar_contato(contato_id)

    if contato is None:
        return False

    executar(
        """
        DELETE FROM CONTATOS_EMERGENCIA
        WHERE ID = :contato_id
        """,
        {"contato_id": contato_id}
    )

    return True

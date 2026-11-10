
from app.services.db_helper import consultar, executar, inserir


def listar_acompanhamentos():
    sql = """
        SELECT *
        FROM ACOMPANHAMENTOS
        ORDER BY ID
    """
    return consultar(sql)


def buscar_acompanhamento(acompanhamento_id: int):
    sql = """
        SELECT *
        FROM ACOMPANHAMENTOS
        WHERE ID = :acompanhamento_id
    """
    return consultar(
        sql,
        {"acompanhamento_id": acompanhamento_id},
        unico=True
    )


def listar_acompanhamentos_usuario(usuario_id: int):
    sql = """
        SELECT *
        FROM ACOMPANHAMENTOS
        WHERE USUARIO_ID = :usuario_id
        ORDER BY ID
    """
    return consultar(sql, {"usuario_id": usuario_id})


def criar_acompanhamento(dados):
    acompanhamento = dados.model_dump()

    sql = """
        INSERT INTO ACOMPANHAMENTOS (
            USUARIO_ID,
            RESPONSAVEL,
            TIPO,
            DESCRICAO,
            DATA_REGISTRO,
            STATUS
        )
        VALUES (
            :usuario_id,
            :responsavel,
            :tipo,
            :descricao,
            :data_registro,
            'REGISTRADO'
        )
        RETURNING ID INTO :id_novo
    """

    novo_id = inserir(sql, acompanhamento)

    resultado = buscar_acompanhamento(novo_id)

    if resultado is None:
        raise Exception(
            "Não foi possível recuperar o acompanhamento cadastrado."
        )

    return resultado


def atualizar_acompanhamento(acompanhamento_id: int, dados):
    acompanhamento = buscar_acompanhamento(acompanhamento_id)

    if acompanhamento is None:
        return None

    dados_atualizados = dados.model_dump(
        exclude_unset=True
    )

    campos_permitidos = {
        "responsavel": "RESPONSAVEL",
        "tipo": "TIPO",
        "descricao": "DESCRICAO",
        "status": "STATUS"
    }

    partes_sql = []
    parametros = {"acompanhamento_id": acompanhamento_id}

    for campo, valor in dados_atualizados.items():
        if campo in campos_permitidos:
            coluna = campos_permitidos[campo]
            parametro = campo

            partes_sql.append(f"{coluna} = :{parametro}")
            parametros[parametro] = valor

    if not partes_sql:
        return acompanhamento

    sql = f"""
        UPDATE ACOMPANHAMENTOS
        SET {", ".join(partes_sql)}
        WHERE ID = :acompanhamento_id
    """

    executar(sql, parametros)

    return buscar_acompanhamento(acompanhamento_id)


def excluir_acompanhamento(acompanhamento_id: int):
    acompanhamento = buscar_acompanhamento(acompanhamento_id)

    if acompanhamento is None:
        return False

    executar(
        """
        DELETE FROM ACOMPANHAMENTOS
        WHERE ID = :acompanhamento_id
        """,
        {"acompanhamento_id": acompanhamento_id}
    )

    return True


from app.services.db_helper import consultar, executar, inserir


def listar_alertas():
    sql = """
        SELECT *
        FROM ALERTAS
        ORDER BY ID
    """
    return consultar(sql)


def buscar_alerta(alerta_id: int):
    sql = """
        SELECT *
        FROM ALERTAS
        WHERE ID = :alerta_id
    """
    return consultar(sql, {"alerta_id": alerta_id}, unico=True)


def listar_alertas_usuario(usuario_id: int):
    sql = """
        SELECT *
        FROM ALERTAS
        WHERE USUARIO_ID = :usuario_id
        ORDER BY ID
    """
    return consultar(sql, {"usuario_id": usuario_id})


def criar_alerta(dados):
    alerta = dados.model_dump()

    sql = """
        INSERT INTO ALERTAS (
            USUARIO_ID,
            CONTATO_ID,
            TIPO,
            DESCRICAO,
            DATA_ALERTA,
            STATUS
        )
        VALUES (
            :usuario_id,
            :contato_id,
            :tipo,
            :descricao,
            :data_alerta,
            'ABERTO'
        )
        RETURNING ID INTO :id_novo
    """

    novo_id = inserir(sql, alerta)

    resultado = buscar_alerta(novo_id)

    if resultado is None:
        raise Exception("Não foi possível recuperar o alerta cadastrado.")

    return resultado


def atualizar_alerta(alerta_id: int, dados):
    alerta = buscar_alerta(alerta_id)

    if alerta is None:
        return None

    dados_atualizados = dados.model_dump(
        exclude_unset=True
    )

    campos_permitidos = {
        "contato_id": "CONTATO_ID",
        "tipo": "TIPO",
        "descricao": "DESCRICAO",
        "status": "STATUS"
    }

    partes_sql = []
    parametros = {"alerta_id": alerta_id}

    for campo, valor in dados_atualizados.items():
        if campo in campos_permitidos:
            coluna = campos_permitidos[campo]
            parametro = campo

            partes_sql.append(f"{coluna} = :{parametro}")
            parametros[parametro] = valor

    if not partes_sql:
        return alerta

    sql = f"""
        UPDATE ALERTAS
        SET {", ".join(partes_sql)}
        WHERE ID = :alerta_id
    """

    executar(sql, parametros)

    return buscar_alerta(alerta_id)


def excluir_alerta(alerta_id: int):
    alerta = buscar_alerta(alerta_id)

    if alerta is None:
        return False

    executar(
        """
        DELETE FROM ALERTAS
        WHERE ID = :alerta_id
        """,
        {"alerta_id": alerta_id}
    )

    return True

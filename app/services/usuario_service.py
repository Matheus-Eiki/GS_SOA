
import hashlib
import secrets

from app.database.connection import conectar
from app.services.db_helper import consultar, executar, inserir


# ==========================================
# GERAR HASH DA SENHA
# ==========================================

def gerar_hash_senha(senha: str):
    salt = secrets.token_hex(16)

    hash_senha = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode("utf-8"),
        salt.encode("utf-8"),
        600000
    )

    return f"{salt}${hash_senha.hex()}"


# ==========================================
# LISTAR TODOS OS USUÁRIOS ATIVOS
# ==========================================

def listar_usuarios():
    sql = """
        SELECT
            ID,
            NOME,
            EMAIL,
            TELEFONE,
            DATA_NASCIMENTO,
            ENDERECO,
            MORA_SOZINHO,
            NECESSIDADES_ACESSIBILIDADE,
            ATIVO,
            DATA_CADASTRO
        FROM USUARIOS
        WHERE ATIVO = 1
        ORDER BY ID
    """

    return consultar(sql)


# ==========================================
# BUSCAR USUÁRIO PELO ID
# ==========================================

def buscar_usuario(usuario_id: int):
    sql = """
        SELECT
            ID,
            NOME,
            EMAIL,
            TELEFONE,
            DATA_NASCIMENTO,
            ENDERECO,
            MORA_SOZINHO,
            NECESSIDADES_ACESSIBILIDADE,
            ATIVO,
            DATA_CADASTRO
        FROM USUARIOS
        WHERE ID = :usuario_id
        AND ATIVO = 1
    """

    return consultar(
        sql,
        {"usuario_id": usuario_id},
        unico=True
    )


# ==========================================
# CADASTRAR USUÁRIO
# ==========================================

def criar_usuario(dados):
    usuario = dados.model_dump()

    senha = usuario.pop("senha")
    senha_hash = gerar_hash_senha(senha)

    sql = """
        INSERT INTO USUARIOS (
            NOME,
            EMAIL,
            TELEFONE,
            DATA_NASCIMENTO,
            ENDERECO,
            MORA_SOZINHO,
            NECESSIDADES_ACESSIBILIDADE,
            SENHA_HASH,
            ATIVO
        )
        VALUES (
            :nome,
            :email,
            :telefone,
            :data_nascimento,
            :endereco,
            :mora_sozinho,
            :necessidades_acessibilidade,
            :senha_hash,
            1
        )
        RETURNING ID INTO :id_novo
    """

    usuario["senha_hash"] = senha_hash

    novo_id = inserir(sql, usuario)

    resultado = buscar_usuario(novo_id)

    if resultado is None:
        raise Exception(
            "Usuário cadastrado, mas não foi possível recuperar seus dados."
        )

    return resultado


# ==========================================
# ATUALIZAR USUÁRIO
# ==========================================

def atualizar_usuario(usuario_id: int, dados):
    usuario = buscar_usuario(usuario_id)

    if usuario is None:
        return None

    dados_atualizados = dados.model_dump(
        exclude_unset=True,
        exclude_none=True
    )

    campos_permitidos = {
        "nome": "NOME",
        "email": "EMAIL",
        "telefone": "TELEFONE",
        "data_nascimento": "DATA_NASCIMENTO",
        "endereco": "ENDERECO",
        "mora_sozinho": "MORA_SOZINHO",
        "necessidades_acessibilidade": "NECESSIDADES_ACESSIBILIDADE"
    }

    atualizacoes = {}

    for campo, valor in dados_atualizados.items():

        if campo == "senha":
            atualizacoes["SENHA_HASH"] = gerar_hash_senha(valor)

        elif campo in campos_permitidos:
            coluna = campos_permitidos[campo]
            atualizacoes[coluna] = valor

    if not atualizacoes:
        return usuario

    partes_sql = []

    parametros = {
        "usuario_id": usuario_id
    }

    for coluna, valor in atualizacoes.items():
        nome_parametro = coluna.lower()

        partes_sql.append(
            f"{coluna} = :{nome_parametro}"
        )

        parametros[nome_parametro] = valor

    sql = f"""
        UPDATE USUARIOS
        SET {", ".join(partes_sql)}
        WHERE ID = :usuario_id
        AND ATIVO = 1
    """

    executar(sql, parametros)

    return buscar_usuario(usuario_id)


# ==========================================
# EXCLUIR USUÁRIO E REGISTROS RELACIONADOS
# ==========================================

def excluir_usuario(usuario_id: int):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        # Verifica se o usuário existe
        cursor.execute(
            """
            SELECT ID
            FROM USUARIOS
            WHERE ID = :usuario_id
            """,
            {"usuario_id": usuario_id}
        )

        usuario = cursor.fetchone()

        if usuario is None:
            return False

        # 1. Exclui os alertas
        cursor.execute(
            """
            DELETE FROM ALERTAS
            WHERE USUARIO_ID = :usuario_id
            """,
            {"usuario_id": usuario_id}
        )

        # 2. Exclui os acompanhamentos
        cursor.execute(
            """
            DELETE FROM ACOMPANHAMENTOS
            WHERE USUARIO_ID = :usuario_id
            """,
            {"usuario_id": usuario_id}
        )

        # 3. Exclui os contatos de emergência
        cursor.execute(
            """
            DELETE FROM CONTATOS_EMERGENCIA
            WHERE USUARIO_ID = :usuario_id
            """,
            {"usuario_id": usuario_id}
        )

        # 4. Exclui o usuário
        cursor.execute(
            """
            DELETE FROM USUARIOS
            WHERE ID = :usuario_id
            """,
            {"usuario_id": usuario_id}
        )

        # Confirma todas as exclusões no Oracle
        conexao.commit()

        return True

    except Exception:
        conexao.rollback()
        raise

    finally:
        cursor.close()
        conexao.close()

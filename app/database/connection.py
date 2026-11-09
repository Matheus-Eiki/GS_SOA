
import os
import oracledb

from dotenv import load_dotenv

load_dotenv()


def conectar():
    usuario = os.getenv("DB_USER")
    senha = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    porta = os.getenv("DB_PORT")
    servico = os.getenv("DB_SERVICE")

    dsn = f"{host}:{porta}/{servico}"

    conexao = oracledb.connect(
        user=usuario,
        password=senha,
        dsn=dsn
    )

    return conexao

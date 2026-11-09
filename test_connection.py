
from app.database.connection import conectar

try:
    conexao = conectar()

    print("Conexão com Oracle realizada com sucesso!")

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM USUARIOS
    """)

    resultado = cursor.fetchone()

    print(f"Quantidade de usuários cadastrados: {resultado[0]}")

    cursor.close()
    conexao.close()

except Exception as erro:
    print("Erro ao conectar com Oracle:")
    print(erro)

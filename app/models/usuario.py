
from sqlalchemy import Column, Integer, String, Date, DateTime
from app.models.base import Base


class Usuario(Base):
    __tablename__ = "USUARIOS"

    id = Column("ID", Integer, primary_key=True)
    nome = Column("NOME", String(150), nullable=False)
    email = Column("EMAIL", String(150), nullable=False, unique=True)
    telefone = Column("TELEFONE", String(20))
    data_nascimento = Column("DATA_NASCIMENTO", Date)
    endereco = Column("ENDERECO", String(255))
    mora_sozinho = Column("MORA_SOZINHO", Integer, nullable=False, default=0)
    necessidades_acessibilidade = Column(
        "NECESSIDADES_ACESSIBILIDADE", String(500)
    )
    senha_hash = Column("SENHA_HASH", String(255), nullable=False)
    ativo = Column("ATIVO", Integer, nullable=False, default=1)
    data_cadastro = Column("DATA_CADASTRO", DateTime)

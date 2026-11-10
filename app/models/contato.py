from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import Base


class Contato(Base):
    __tablename__ = "CONTATOS_EMERGENCIA"

    id = Column("ID", Integer, primary_key=True)
    usuario_id = Column(
        "USUARIO_ID",
        Integer,
        ForeignKey("USUARIOS.ID"),
        nullable=False
    )
    nome = Column("NOME", String(150), nullable=False)
    parentesco = Column("PARENTESCO", String(50))
    telefone = Column("TELEFONE", String(20), nullable=False)
    email = Column("EMAIL", String(150))
    principal = Column("PRINCIPAL", Integer, nullable=False, default=0)
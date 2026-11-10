from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.models.base import Base


class Alerta(Base):
    __tablename__ = "ALERTAS"

    id = Column("ID", Integer, primary_key=True)
    usuario_id = Column(
        "USUARIO_ID",
        Integer,
        ForeignKey("USUARIOS.ID"),
        nullable=False
    )
    contato_id = Column(
        "CONTATO_ID",
        Integer,
        ForeignKey("CONTATOS_EMERGENCIA.ID"),
        nullable=True
    )
    tipo = Column("TIPO", String(30), nullable=False)
    descricao = Column("DESCRICAO", String(500), nullable=False)
    data_alerta = Column("DATA_ALERTA", DateTime, nullable=False)
    status = Column("STATUS", String(30), nullable=False, default="ABERTO")
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.models.base import Base


class Acompanhamento(Base):
    __tablename__ = "ACOMPANHAMENTOS"

    id = Column("ID", Integer, primary_key=True)
    usuario_id = Column(
        "USUARIO_ID",
        Integer,
        ForeignKey("USUARIOS.ID"),
        nullable=False
    )
    responsavel = Column("RESPONSAVEL", String(150), nullable=False)
    tipo = Column("TIPO", String(50), nullable=False)
    descricao = Column("DESCRICAO", String(500))
    data_registro = Column("DATA_REGISTRO", DateTime, nullable=False)
    status = Column("STATUS", String(30), nullable=False, default="REGISTRADO")
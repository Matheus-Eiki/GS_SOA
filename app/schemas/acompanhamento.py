
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Literal


StatusAcompanhamento = Literal[
    "REGISTRADO",
    "CANCELADO"
]


class AcompanhamentoCreate(BaseModel):
    usuario_id: int
    responsavel: str
    tipo: str
    descricao: Optional[str] = None


class AcompanhamentoUpdate(BaseModel):
    responsavel: Optional[str] = None
    tipo: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[StatusAcompanhamento] = None


class AcompanhamentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    responsavel: str
    tipo: str
    descricao: Optional[str] = None
    data_registro: datetime
    status: StatusAcompanhamento

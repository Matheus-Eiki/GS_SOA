
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Literal


TipoAlerta = Literal[
    "EMERGENCIA",
    "ASSISTENCIA",
    "LEMBRETE"
]

StatusAlerta = Literal[
    "ABERTO",
    "EM_ATENDIMENTO",
    "RESOLVIDO",
    "CANCELADO"
]


class AlertaCreate(BaseModel):
    usuario_id: int
    contato_id: Optional[int] = None
    tipo: TipoAlerta
    descricao: str
    data_alerta: datetime


class AlertaUpdate(BaseModel):
    contato_id: Optional[int] = None
    tipo: Optional[TipoAlerta] = None
    descricao: Optional[str] = None
    status: Optional[StatusAlerta] = None


class AlertaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    contato_id: Optional[int] = None
    tipo: TipoAlerta
    descricao: str
    data_alerta: datetime
    status: StatusAlerta

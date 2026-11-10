
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class ContatoCreate(BaseModel):
    usuario_id: int
    nome: str
    parentesco: Optional[str] = None
    telefone: str
    email: Optional[str] = None
    principal: int = Field(default=0, ge=0, le=1)


class ContatoUpdate(BaseModel):
    nome: Optional[str] = None
    parentesco: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    principal: Optional[int] = Field(default=None, ge=0, le=1)


class ContatoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    nome: str
    parentesco: Optional[str] = None
    telefone: str
    email: Optional[str] = None
    principal: int

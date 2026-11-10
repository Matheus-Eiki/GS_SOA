
from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional


class UsuarioCreate(BaseModel):
    nome: str
    email: str
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None
    endereco: Optional[str] = None
    mora_sozinho: int = Field(default=0, ge=0, le=1)
    necessidades_acessibilidade: Optional[str] = None
    senha: str = Field(min_length=8)


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None
    endereco: Optional[str] = None
    mora_sozinho: Optional[int] = Field(default=None, ge=0, le=1)
    necessidades_acessibilidade: Optional[str] = None
    senha: Optional[str] = Field(default=None, min_length=8)
    ativo: Optional[int] = Field(default=None, ge=0, le=1)


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: str
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None
    endereco: Optional[str] = None
    mora_sozinho: int
    necessidades_acessibilidade: Optional[str] = None
    ativo: int
    data_cadastro: Optional[datetime] = None

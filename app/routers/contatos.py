
from fastapi import APIRouter, HTTPException

from app.schemas.contato import (
    ContatoCreate,
    ContatoUpdate,
    ContatoResponse
)

from app.services import contato_service


router = APIRouter(
    prefix="/contatos",
    tags=["Contatos de Emergência"]
)


@router.post("/", response_model=ContatoResponse, status_code=201)
def cadastrar_contato(dados: ContatoCreate):
    try:
        return contato_service.criar_contato(dados)
    except Exception as erro:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao cadastrar contato: {str(erro)}"
        )


@router.get("/", response_model=list[ContatoResponse])
def listar_contatos():
    return contato_service.listar_contatos()


@router.get("/usuario/{usuario_id}", response_model=list[ContatoResponse])
def listar_contatos_usuario(usuario_id: int):
    return contato_service.listar_contatos_usuario(usuario_id)


@router.get("/{contato_id}", response_model=ContatoResponse)
def buscar_contato(contato_id: int):
    contato = contato_service.buscar_contato(contato_id)

    if contato is None:
        raise HTTPException(
            status_code=404,
            detail="Contato não encontrado."
        )

    return contato


@router.put("/{contato_id}", response_model=ContatoResponse)
def atualizar_contato(contato_id: int, dados: ContatoUpdate):
    try:
        contato = contato_service.atualizar_contato(contato_id, dados)

        if contato is None:
            raise HTTPException(
                status_code=404,
                detail="Contato não encontrado."
            )

        return contato

    except HTTPException:
        raise
    except Exception as erro:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao atualizar contato: {str(erro)}"
        )


@router.delete("/{contato_id}")
def excluir_contato(contato_id: int):
    try:
        resultado = contato_service.excluir_contato(contato_id)

        if not resultado:
            raise HTTPException(
                status_code=404,
                detail="Contato não encontrado."
            )

        return {
            "mensagem": "Contato excluído com sucesso!"
        }

    except HTTPException:
        raise
    except Exception as erro:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao excluir contato: {str(erro)}"
        )

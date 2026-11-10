
from fastapi import APIRouter, HTTPException

from app.schemas.acompanhamento import (
    AcompanhamentoCreate,
    AcompanhamentoUpdate,
    AcompanhamentoResponse
)

from app.services import acompanhamento_service


router = APIRouter(
    prefix="/acompanhamentos",
    tags=["Acompanhamentos"]
)


@router.post("/", response_model=AcompanhamentoResponse, status_code=201)
def cadastrar_acompanhamento(dados: AcompanhamentoCreate):
    try:
        return acompanhamento_service.criar_acompanhamento(dados)
    except Exception as erro:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao cadastrar acompanhamento: {str(erro)}"
        )


@router.get("/", response_model=list[AcompanhamentoResponse])
def listar_acompanhamentos():
    return acompanhamento_service.listar_acompanhamentos()


@router.get("/usuario/{usuario_id}", response_model=list[AcompanhamentoResponse])
def listar_acompanhamentos_usuario(usuario_id: int):
    return acompanhamento_service.listar_acompanhamentos_usuario(usuario_id)


@router.get("/{acompanhamento_id}", response_model=AcompanhamentoResponse)
def buscar_acompanhamento(acompanhamento_id: int):
    acompanhamento = acompanhamento_service.buscar_acompanhamento(
        acompanhamento_id
    )

    if acompanhamento is None:
        raise HTTPException(
            status_code=404,
            detail="Acompanhamento não encontrado."
        )

    return acompanhamento


@router.put("/{acompanhamento_id}", response_model=AcompanhamentoResponse)
def atualizar_acompanhamento(
    acompanhamento_id: int,
    dados: AcompanhamentoUpdate
):
    try:
        acompanhamento = acompanhamento_service.atualizar_acompanhamento(
            acompanhamento_id,
            dados
        )

        if acompanhamento is None:
            raise HTTPException(
                status_code=404,
                detail="Acompanhamento não encontrado."
            )

        return acompanhamento

    except HTTPException:
        raise
    except Exception as erro:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao atualizar acompanhamento: {str(erro)}"
        )


@router.delete("/{acompanhamento_id}")
def excluir_acompanhamento(acompanhamento_id: int):
    try:
        resultado = acompanhamento_service.excluir_acompanhamento(
            acompanhamento_id
        )

        if not resultado:
            raise HTTPException(
                status_code=404,
                detail="Acompanhamento não encontrado."
            )

        return {
            "mensagem": "Acompanhamento excluído com sucesso!"
        }

    except HTTPException:
        raise
    except Exception as erro:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao excluir acompanhamento: {str(erro)}"
        )

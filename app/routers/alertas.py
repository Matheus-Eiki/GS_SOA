
from fastapi import APIRouter, HTTPException

from app.schemas.alerta import (
    AlertaCreate,
    AlertaUpdate,
    AlertaResponse
)

from app.services import alerta_service


router = APIRouter(
    prefix="/alertas",
    tags=["Alertas"]
)


@router.post("/", response_model=AlertaResponse, status_code=201)
def cadastrar_alerta(dados: AlertaCreate):
    try:
        return alerta_service.criar_alerta(dados)
    except Exception as erro:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao cadastrar alerta: {str(erro)}"
        )


@router.get("/", response_model=list[AlertaResponse])
def listar_alertas():
    return alerta_service.listar_alertas()


@router.get("/usuario/{usuario_id}", response_model=list[AlertaResponse])
def listar_alertas_usuario(usuario_id: int):
    return alerta_service.listar_alertas_usuario(usuario_id)


@router.get("/{alerta_id}", response_model=AlertaResponse)
def buscar_alerta(alerta_id: int):
    alerta = alerta_service.buscar_alerta(alerta_id)

    if alerta is None:
        raise HTTPException(
            status_code=404,
            detail="Alerta não encontrado."
        )

    return alerta


@router.put("/{alerta_id}", response_model=AlertaResponse)
def atualizar_alerta(alerta_id: int, dados: AlertaUpdate):
    try:
        alerta = alerta_service.atualizar_alerta(alerta_id, dados)

        if alerta is None:
            raise HTTPException(
                status_code=404,
                detail="Alerta não encontrado."
            )

        return alerta

    except HTTPException:
        raise
    except Exception as erro:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao atualizar alerta: {str(erro)}"
        )


@router.delete("/{alerta_id}")
def excluir_alerta(alerta_id: int):
    try:
        resultado = alerta_service.excluir_alerta(alerta_id)

        if not resultado:
            raise HTTPException(
                status_code=404,
                detail="Alerta não encontrado."
            )

        return {
            "mensagem": "Alerta excluído com sucesso!"
        }

    except HTTPException:
        raise
    except Exception as erro:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao excluir alerta: {str(erro)}"
        )

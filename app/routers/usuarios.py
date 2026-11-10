
from fastapi import APIRouter, HTTPException, status

from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse
)

from app.services import usuario_service


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_usuario(dados: UsuarioCreate):
    try:
        return usuario_service.criar_usuario(dados)

    except Exception as erro:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao cadastrar usuário: {str(erro)}"
        )


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios():
    return usuario_service.listar_usuarios()


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def buscar_usuario(usuario_id: int):
    usuario = usuario_service.buscar_usuario(usuario_id)

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado."
        )

    return usuario


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(usuario_id: int, dados: UsuarioUpdate):
    try:
        usuario = usuario_service.atualizar_usuario(
            usuario_id,
            dados
        )

        if usuario is None:
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado."
            )

        return usuario

    except HTTPException:
        raise

    except Exception as erro:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao atualizar usuário: {str(erro)}"
        )


@router.delete("/{usuario_id}")
def excluir_usuario(usuario_id: int):
    try:
        resultado = usuario_service.excluir_usuario(usuario_id)

        if not resultado:
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado."
            )

        return {
            "mensagem": "Usuário e todos os seus registros relacionados foram excluídos permanentemente."
        }

    except HTTPException:
        raise

    except Exception as erro:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao excluir usuário: {str(erro)}"
        )

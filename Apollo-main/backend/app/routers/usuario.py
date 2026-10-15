from fastapi import APIRouter, Depends

from app.models import Usuario
from app.schemas import UsuarioOut
from app.security import get_current_user

router = APIRouter(prefix="/api/usuario", tags=["usuário"])


@router.get("/atual", response_model=UsuarioOut)
def usuario_atual(usuario: Usuario = Depends(get_current_user)):
    return UsuarioOut(nome=usuario.nome, papel=usuario.papel.value, iniciais=usuario.iniciais)

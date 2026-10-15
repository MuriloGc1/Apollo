from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Usuario
from app.schemas import LoginIn, LoginOut, RecuperarSenhaIn, MensagemGenericaOut, UsuarioOut
from app.security import verificar_senha, criar_access_token

router = APIRouter(prefix="/api/auth", tags=["autenticação"])


@router.post("/login", response_model=LoginOut)
def login(dados: LoginIn, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="E-mail ou senha incorretos")

    token = criar_access_token(usuario.id)
    return LoginOut(
        access_token=token,
        usuario=UsuarioOut(nome=usuario.nome, papel=usuario.papel.value, iniciais=usuario.iniciais),
    )


@router.post("/recuperar-senha", response_model=MensagemGenericaOut)
def recuperar_senha(dados: RecuperarSenhaIn, db: Session = Depends(get_db)):
    db.query(Usuario).filter(Usuario.email == dados.email).first()
    return MensagemGenericaOut(mensagem="Se o e-mail existir na nossa base, um link de redefinição foi enviado.")

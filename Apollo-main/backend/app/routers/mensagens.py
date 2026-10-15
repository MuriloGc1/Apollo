from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Conversa, Mensagem, Usuario
from app.schemas import ContatoOut, MensagemOut, MensagemIn
from app.security import get_current_user
from app.formatadores import hora_relativa, hora

router = APIRouter(prefix="/api", tags=["mensagens"])


@router.get("/contatos", response_model=list[ContatoOut])
def listar_contatos(db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    agora = datetime.now(timezone.utc)
    conversas = (
        db.query(Conversa)
        .options(joinedload(Conversa.mensagens))
        .filter(Conversa.aluno_id == usuario.id)
        .all()
    )

    conversas_com_data = [(c, c.mensagens[-1].criado_em if c.mensagens else None) for c in conversas]
    conversas_com_data.sort(key=lambda par: par[1] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)

    return [
        ContatoOut(
            id=str(c.id),
            iniciais=c.iniciais,
            corBg=c.cor_bg,
            corTexto=c.cor_texto,
            nome=c.nome_exibicao,
            info=c.outro_usuario.papel.value.capitalize() if c.outro_usuario else "Grupo da turma",
            hora=hora_relativa(ultima_data, agora) if ultima_data else "",
            ativo=False,
        )
        for c, ultima_data in conversas_com_data
    ]


@router.get("/mensagens/{conversa_id}", response_model=list[MensagemOut])
def listar_mensagens(
    conversa_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)
):
    conversa = db.query(Conversa).filter(Conversa.id == conversa_id, Conversa.aluno_id == usuario.id).first()
    if not conversa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversa não encontrada")

    return [
        MensagemOut(
            direcao="sent" if m.remetente_id == usuario.id else "recv",
            texto=m.texto,
            hora=hora(m.criado_em),
        )
        for m in conversa.mensagens
    ]


@router.post("/mensagens/{conversa_id}", response_model=MensagemOut, status_code=status.HTTP_201_CREATED)
def enviar_mensagem(
    conversa_id: int, dados: MensagemIn, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)
):
    conversa = db.query(Conversa).filter(Conversa.id == conversa_id, Conversa.aluno_id == usuario.id).first()
    if not conversa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversa não encontrada")

    nova = Mensagem(conversa_id=conversa_id, remetente_id=usuario.id, texto=dados.texto)
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return MensagemOut(direcao="sent", texto=nova.texto, hora=hora(nova.criado_em))

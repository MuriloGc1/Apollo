from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import EventoAgenda, Usuario
from app.schemas import EventoOut, EventoCalendarioOut
from app.security import get_current_user
from app.formatadores import hora, data_evento_proximo

router = APIRouter(prefix="/api/eventos", tags=["agenda"])


def _inicio_do_dia(dt: datetime) -> datetime:
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


@router.get("/hoje", response_model=list[EventoOut])
def eventos_hoje(db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    agora = datetime.now(timezone.utc)
    inicio = _inicio_do_dia(agora)
    fim = inicio + timedelta(days=1)
    eventos = (
        db.query(EventoAgenda)
        .filter(EventoAgenda.aluno_id == usuario.id, EventoAgenda.data_hora >= inicio, EventoAgenda.data_hora < fim)
        .order_by(EventoAgenda.data_hora)
        .all()
    )
    return [EventoOut(cor=e.cor, hora=hora(e.data_hora), nome=e.nome) for e in eventos]


@router.get("/proximos", response_model=list[EventoOut])
def proximos_eventos(db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    amanha = _inicio_do_dia(datetime.now(timezone.utc)) + timedelta(days=1)
    eventos = (
        db.query(EventoAgenda)
        .filter(EventoAgenda.aluno_id == usuario.id, EventoAgenda.data_hora >= amanha)
        .order_by(EventoAgenda.data_hora)
        .limit(5)
        .all()
    )
    return [EventoOut(cor=e.cor, hora=data_evento_proximo(e.data_hora), nome=e.nome) for e in eventos]


@router.get("/calendario", response_model=list[EventoCalendarioOut])
def eventos_calendario(db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    eventos = db.query(EventoAgenda).filter(EventoAgenda.aluno_id == usuario.id).all()
    return [EventoCalendarioOut(dia=e.data_hora.day, mes=e.data_hora.month - 1, ano=e.data_hora.year) for e in eventos]

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status as http_status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Tarefa, Usuario
from app.schemas import TarefaOut, TarefaStatusIn
from app.security import get_current_user
from app.formatadores import data_hora_curta, data_curta
from app import regras

router = APIRouter(prefix="/api/tarefas", tags=["tarefas"])


def _montar_saida(t: Tarefa) -> TarefaOut:
    agora = datetime.now(timezone.utc)
    status_atual = regras.status_tarefa(t.entregue_em, t.prazo, agora)
    data_label = (
        f"Entregue em: {data_curta(t.entregue_em)}" if status_atual == "entregue" else f"Data: {data_hora_curta(t.prazo)}"
    )
    return TarefaOut(id=t.id, disciplina=t.materia.nome, status=status_atual, descricao=t.descricao, dataLabel=data_label)


@router.get("", response_model=list[TarefaOut])
def listar_tarefas(db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    tarefas = (
        db.query(Tarefa)
        .options(joinedload(Tarefa.materia))
        .filter(Tarefa.aluno_id == usuario.id)
        .order_by(Tarefa.prazo)
        .all()
    )
    return [_montar_saida(t) for t in tarefas]


@router.patch("/{tarefa_id}/status", response_model=TarefaOut)
def marcar_status(
    tarefa_id: int, dados: TarefaStatusIn, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)
):
    if dados.status != "entregue":
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail='Só é possível marcar como "entregue"')

    tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id, Tarefa.aluno_id == usuario.id).first()
    if not tarefa:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")

    tarefa.entregue_em = datetime.now(timezone.utc)
    db.commit()
    db.refresh(tarefa)
    return _montar_saida(tarefa)

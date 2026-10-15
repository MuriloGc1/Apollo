from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Matricula, Usuario
from app.schemas import NotaLinhaOut, ProgressoItemOut
from app.security import get_current_user
from app import regras

router = APIRouter(tags=["notas"])


def _fmt(valor: float) -> str:
    return f"{valor:.1f}".replace(".", ",")


@router.get("/api/notas", response_model=list[NotaLinhaOut])
def listar_notas(bimestre: int = 1, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    matriculas = (
        db.query(Matricula)
        .options(joinedload(Matricula.materia), joinedload(Matricula.professor), joinedload(Matricula.notas))
        .filter(Matricula.aluno_id == usuario.id)
        .all()
    )

    resultado = []
    for m in matriculas:
        nota = next((n for n in m.notas if n.bimestre == bimestre), None)
        if not nota:
            continue
        av1, av2, av3 = float(nota.av1), float(nota.av2), float(nota.av3)
        total = round((av1 + av2 + av3) / 3, 1)

        resultado.append(
            NotaLinhaOut(
                disciplina=m.materia.nome,
                corDot=m.materia.cor,
                professor=m.professor.nome,
                faltas=nota.faltas,
                statusFaltas=regras.status_faltas_boletim(nota.faltas),
                av1=_fmt(av1),
                av2=_fmt(av2),
                av3=_fmt(av3),
                total=_fmt(total),
                statusValores=regras.status_nota_boletim(total),
                statusTotal=regras.status_nota_boletim(total),
                statusAv1=regras.status_nota_boletim(av1),
                statusAv2=regras.status_nota_boletim(av2),
                statusAv3=regras.status_nota_boletim(av3),
            )
        )
    return resultado


@router.get("/api/progresso-disciplinas", response_model=list[ProgressoItemOut])
def progresso_disciplinas(db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    matriculas = db.query(Matricula).options(joinedload(Matricula.materia)).filter(Matricula.aluno_id == usuario.id).all()
    return [
        ProgressoItemOut(nome=m.materia.nome, pct=m.progresso_percentual, cor=m.cor_progresso) for m in matriculas
    ]


@router.get("/api/frequencia-disciplinas", response_model=list[ProgressoItemOut])
def frequencia_disciplinas(db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    matriculas = db.query(Matricula).options(joinedload(Matricula.materia)).filter(Matricula.aluno_id == usuario.id).all()
    return [
        ProgressoItemOut(
            nome=m.materia.nome,
            pct=round(float(m.frequencia_percentual)),
            cor="#f97316" if regras.status_frequencia(float(m.frequencia_percentual)) != "green" else None,
        )
        for m in matriculas
    ]

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Matricula, Usuario
from app.schemas import DisciplinaOut
from app.security import get_current_user
from app import regras

router = APIRouter(prefix="/api/disciplinas", tags=["disciplinas"])


@router.get("", response_model=list[DisciplinaOut])
def listar_disciplinas(db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    matriculas = (
        db.query(Matricula)
        .options(joinedload(Matricula.materia), joinedload(Matricula.professor), joinedload(Matricula.notas))
        .filter(Matricula.aluno_id == usuario.id)
        .all()
    )

    resultado = []
    for m in matriculas:
        ultima_nota = m.notas[-1] if m.notas else None
        media = float((ultima_nota.av1 + ultima_nota.av2 + ultima_nota.av3) / 3) if ultima_nota else 0.0
        faltas = ultima_nota.faltas if ultima_nota else 0

        resultado.append(
            DisciplinaOut(
                nome=m.materia.nome,
                professor=m.professor.nome,
                iniciais=m.professor.iniciais,
                corAvatar=m.professor.cor_avatar,
                media=f"{media:.1f}".replace(".", ","),
                statusMedia=regras.status_nota_disciplina(media),
                faltas=faltas,
                statusFaltas=regras.status_faltas_disciplina(faltas),
                frequencia=f"{float(m.frequencia_percentual):.0f}%",
                statusFrequencia=regras.status_frequencia(float(m.frequencia_percentual)),
                progresso=m.progresso_percentual,
                corProgresso=m.cor_progresso,
            )
        )
    return resultado

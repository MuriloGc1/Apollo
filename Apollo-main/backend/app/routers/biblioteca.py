from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import MaterialBiblioteca, FavoritoBiblioteca, Usuario
from app.schemas import MaterialBibliotecaOut, FavoritoIn
from app.security import get_current_user

router = APIRouter(prefix="/api/biblioteca", tags=["biblioteca"])


def _favoritos_do_aluno(db: Session, aluno_id: int) -> set[int]:
    linhas = db.query(FavoritoBiblioteca.material_id).filter(FavoritoBiblioteca.aluno_id == aluno_id).all()
    return {material_id for (material_id,) in linhas}


@router.get("", response_model=list[MaterialBibliotecaOut])
def listar_biblioteca(db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    materiais = db.query(MaterialBiblioteca).options(joinedload(MaterialBiblioteca.materia)).all()
    favoritos = _favoritos_do_aluno(db, usuario.id)

    return [
        MaterialBibliotecaOut(
            id=m.id,
            sigla=m.sigla,
            gradiente=[m.cor_gradiente_1, m.cor_gradiente_2],
            subtitulo=m.subtitulo,
            nome=m.nome,
            professor=m.professor.nome,
            badge={"texto": m.badge_texto, "bg": m.badge_bg, "cor": m.badge_cor},
            tipos=m.tipos,
            favorito=m.id in favoritos,
        )
        for m in materiais
    ]


@router.patch("/{material_id}/favorito", status_code=status.HTTP_204_NO_CONTENT)
def definir_favorito(
    material_id: int, dados: FavoritoIn, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)
):
    material = db.get(MaterialBiblioteca, material_id)
    if not material:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material não encontrado")

    existente = db.get(FavoritoBiblioteca, {"aluno_id": usuario.id, "material_id": material_id})
    if dados.favorito and not existente:
        db.add(FavoritoBiblioteca(aluno_id=usuario.id, material_id=material_id))
        db.commit()
    elif not dados.favorito and existente:
        db.delete(existente)
        db.commit()

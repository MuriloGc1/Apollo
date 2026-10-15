from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Aviso, Usuario
from app.schemas import AvisoOut
from app.security import get_current_user
from app.formatadores import data_hora_curta

router = APIRouter(prefix="/api/avisos", tags=["avisos"])


@router.get("", response_model=list[AvisoOut])
def listar_avisos(db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)):
    avisos = db.query(Aviso).order_by(Aviso.data_hora.desc()).all()
    return [AvisoOut(icone=a.icone, data=data_hora_curta(a.data_hora), titulo=a.titulo) for a in avisos]

"""Router de estatísticas."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app import schemas, crud
from app.deps import get_current_user
from app.models import User

router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.get("", response_model=schemas.StatisticsOut)
def get_statistics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Obtém estatísticas do usuário.
    
    Se não existir, cria estatísticas padrão.
    """
    statistics = crud.get_user_statistics(db, current_user.id)
    
    if not statistics:
        statistics = crud.create_default_statistics(db, current_user.id)
    
    return statistics


@router.post("", response_model=schemas.StatisticsOut)
def update_statistics(
    statistics: schemas.StatisticsIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza estatísticas do usuário.
    
    Cria estatísticas se não existirem.
    """
    db_statistics = crud.upsert_statistics(db, current_user.id, statistics)
    return db_statistics



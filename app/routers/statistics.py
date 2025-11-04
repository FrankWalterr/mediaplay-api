"""Router de estatísticas."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app import schemas, crud
from app.deps import get_current_user, get_optional_user
from app.models import User, Statistics

router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.get("", response_model=schemas.StatisticsOut)
def get_statistics(
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    Obtém estatísticas (público).
    Se autenticado, retorna estatísticas do usuário.
    Se não autenticado, retorna todas as estatísticas (primeira encontrada).
    """
    if current_user:
        statistics = crud.get_user_statistics(db, current_user.id)
        if not statistics:
            statistics = crud.create_default_statistics(db, current_user.id)
    else:
        # Se não autenticado, retorna primeira estatística encontrada
        statistics = db.query(Statistics).first()
        if not statistics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhuma estatística encontrada"
            )
    
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




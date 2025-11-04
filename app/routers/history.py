"""Router de histórico."""
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app import schemas, crud
from app.deps import get_current_user, get_optional_user
from app.models import User, HistoryItem

router = APIRouter(prefix="/history", tags=["History"])


@router.get("", response_model=List[schemas.HistoryItemOut])
def get_history(
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    Lista todo o histórico de reprodução (público).
    Se autenticado, retorna apenas o histórico do usuário.
    Se não autenticado, retorna todo o histórico.
    """
    if current_user:
        history = crud.get_user_history(db, current_user.id)
    else:
        history = db.query(HistoryItem).all()
    return history


@router.post("", response_model=schemas.HistoryItemOut, status_code=201)
def create_history_item(
    history_item: schemas.HistoryItemIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cria ou atualiza item de histórico (upsert).
    
    Se o item já existir (mesma media_uri + media_type), atualiza e incrementa play_count.
    Caso contrário, cria novo item.
    """
    db_history = crud.upsert_history_item(db, current_user.id, history_item)
    return db_history




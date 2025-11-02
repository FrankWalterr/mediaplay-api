"""Router de histórico."""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app import schemas, crud
from app.deps import get_current_user
from app.models import User

router = APIRouter(prefix="/history", tags=["History"])


@router.get("", response_model=List[schemas.HistoryItemOut])
def get_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Lista todo o histórico de reprodução do usuário.
    """
    history = crud.get_user_history(db, current_user.id)
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



"""Router de configurações."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app import schemas, crud
from app.deps import get_current_user
from app.models import User

router = APIRouter(prefix="/settings", tags=["Settings"])


@router.get("", response_model=schemas.SettingsOut)
def get_settings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Obtém configurações do usuário.
    
    Se não existir, cria configurações padrão.
    """
    settings = crud.get_user_settings(db, current_user.id)
    
    if not settings:
        settings = crud.create_default_settings(db, current_user.id)
    
    return settings


@router.post("", response_model=schemas.SettingsOut)
def update_settings(
    settings: schemas.SettingsIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza configurações do usuário.
    
    Cria configurações se não existirem.
    """
    db_settings = crud.upsert_settings(db, current_user.id, settings)
    return db_settings



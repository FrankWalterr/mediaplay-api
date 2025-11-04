"""Router de configurações."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app import schemas, crud
from app.deps import get_current_user, get_optional_user
from app.models import User, Settings

router = APIRouter(prefix="/settings", tags=["Settings"])


@router.get("", response_model=schemas.SettingsOut)
def get_settings(
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    Obtém configurações (público).
    Se autenticado, retorna configurações do usuário.
    Se não autenticado, retorna todas as configurações (primeira encontrada).
    """
    if current_user:
        settings = crud.get_user_settings(db, current_user.id)
        if not settings:
            settings = crud.create_default_settings(db, current_user.id)
    else:
        # Se não autenticado, retorna primeira configuração encontrada
        settings = db.query(Settings).first()
        if not settings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhuma configuração encontrada"
            )
    
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




"""Router de favoritos."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app import schemas, crud
from app.deps import get_current_user, get_optional_user
from app.models import User, MediaType, Favorite

router = APIRouter(tags=["Favorites"])


@router.get("", response_model=List[schemas.FavoriteOut])
def get_favorites(
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    Lista todos os favoritos (público).
    Se autenticado, retorna apenas os favoritos do usuário.
    Se não autenticado, retorna todos os favoritos.
    """
    if current_user:
        favorites = crud.get_user_favorites(db, current_user.id)
    else:
        favorites = db.query(Favorite).all()
    return favorites


@router.post("", response_model=schemas.FavoriteOut, status_code=status.HTTP_201_CREATED)
def create_favorite(
    favorite: schemas.FavoriteIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cria ou atualiza favorito (upsert).
    
    Se o favorito já existir (mesma media_uri + media_type), atualiza os dados.
    Caso contrário, cria novo favorito.
    """
    db_favorite = crud.upsert_favorite(db, current_user.id, favorite)
    return db_favorite


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite(
    media_uri: str = Query(..., description="URI da mídia"),
    media_type: MediaType = Query(..., description="Tipo da mídia"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deleta favorito específico.
    
    Remove o favorito baseado em media_uri e media_type.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"Tentativa de remover favorito: {media_type} - {media_uri[:50]}...")
    
    deleted = crud.delete_favorite_by_uri(db, current_user.id, media_uri, media_type)
    
    if not deleted:
        logger.warning(f"Favorito não encontrado para usuário {current_user.id}: {media_type} - {media_uri[:50]}...")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorito não encontrado"
        )
    
    logger.info(f"Favorito removido com sucesso: {media_type} - {media_uri[:50]}...")
    return None



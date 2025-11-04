"""Router de tags."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app import schemas, crud
from app.deps import get_current_user, get_optional_user
from app.models import User, Tag

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get("", response_model=List[schemas.TagOut])
def get_tags(
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    Lista todas as tags (público).
    Se autenticado, retorna apenas as tags do usuário.
    Se não autenticado, retorna todas as tags.
    """
    if current_user:
        tags = crud.get_user_tags(db, current_user.id)
    else:
        tags = db.query(Tag).all()
    return tags


@router.post("", response_model=schemas.TagOut, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag: schemas.TagIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cria nova tag.
    """
    db_tag = crud.create_tag(db, current_user.id, tag)
    return db_tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deleta tag.
    """
    deleted = crud.delete_tag(db, tag_id, current_user.id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag não encontrada"
        )
    
    return None


# ==================== MEDIA TAGS ====================

@router.post("/media", response_model=schemas.MediaTagOut, status_code=status.HTTP_201_CREATED)
def link_media_tag(
    media_tag: schemas.MediaTagIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Vincula tag a uma mídia.
    
    Cria vínculo se não existir.
    """
    db_media_tag = crud.create_media_tag(db, media_tag)
    return db_media_tag


@router.delete("/media/{media_tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_media_tag(
    media_tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove vínculo de tag com mídia.
    """
    deleted = crud.delete_media_tag(db, media_tag_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vínculo não encontrado"
        )
    
    return None




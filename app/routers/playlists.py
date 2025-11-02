"""Router de playlists."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app import schemas, crud
from app.deps import get_current_user
from app.models import User

router = APIRouter(prefix="/playlists", tags=["Playlists"])


@router.get("", response_model=List[schemas.PlaylistWithItems])
def get_playlists(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Lista todas as playlists do usuário com seus itens.
    """
    playlists = crud.get_user_playlists(db, current_user.id)
    return playlists


@router.post("", response_model=schemas.PlaylistOut, status_code=status.HTTP_201_CREATED)
def create_playlist(
    playlist: schemas.PlaylistIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cria nova playlist.
    """
    db_playlist = crud.create_playlist(db, current_user.id, playlist)
    return db_playlist


@router.get("/{playlist_id}", response_model=schemas.PlaylistWithItems)
def get_playlist(
    playlist_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtém playlist específica com seus itens.
    """
    playlist = crud.get_playlist(db, playlist_id, current_user.id)
    
    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist não encontrada"
        )
    
    return playlist


@router.put("/{playlist_id}", response_model=schemas.PlaylistOut)
def update_playlist(
    playlist_id: int,
    playlist: schemas.PlaylistIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza playlist existente.
    """
    db_playlist = crud.update_playlist(db, playlist_id, current_user.id, playlist)
    
    if not db_playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist não encontrada"
        )
    
    return db_playlist


@router.delete("/{playlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_playlist(
    playlist_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deleta playlist.
    """
    deleted = crud.delete_playlist(db, playlist_id, current_user.id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist não encontrada"
        )
    
    return None


# ==================== PLAYLIST ITEMS ====================

@router.get("/{playlist_id}/items", response_model=List[schemas.PlaylistItemOut])
def get_playlist_items(
    playlist_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista todos os itens de uma playlist.
    """
    # Verifica se a playlist pertence ao usuário
    playlist = crud.get_playlist(db, playlist_id, current_user.id)
    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist não encontrada"
        )
    
    items = crud.get_playlist_items(db, playlist_id)
    return items


@router.post("/{playlist_id}/items", response_model=schemas.PlaylistItemOut, status_code=status.HTTP_201_CREATED)
def create_playlist_item(
    playlist_id: int,
    item: schemas.PlaylistItemIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Adiciona ou atualiza item na playlist (upsert).
    
    Se o item já existir (mesma media_uri + media_type), atualiza os dados.
    Caso contrário, adiciona novo item.
    """
    # Verifica se a playlist pertence ao usuário
    playlist = crud.get_playlist(db, playlist_id, current_user.id)
    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist não encontrada"
        )
    
    db_item = crud.upsert_playlist_item(db, playlist_id, item)
    return db_item


@router.delete("/{playlist_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_playlist_item(
    playlist_id: int,
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove item específico da playlist.
    """
    # Verifica se a playlist pertence ao usuário
    playlist = crud.get_playlist(db, playlist_id, current_user.id)
    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist não encontrada"
        )
    
    deleted = crud.delete_playlist_item(db, item_id, playlist_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado"
        )
    
    return None



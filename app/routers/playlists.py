"""Router de playlists."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app import schemas, crud
from app.deps import get_current_user, get_optional_user
from app.models import User, Playlist

router = APIRouter(tags=["Playlists"])


@router.get("", response_model=List[schemas.PlaylistWithItems])
def get_playlists(
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    Lista todas as playlists (público).
    Se autenticado, retorna apenas as playlists do usuário.
    Se não autenticado, retorna todas as playlists.
    """
    if current_user:
        # Se autenticado, retorna apenas as do usuário
        playlists = crud.get_user_playlists(db, current_user.id)
    else:
        # Se não autenticado, retorna todas
        playlists = db.query(Playlist).all()
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
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    Obtém playlist específica com seus itens (público).
    """
    if current_user:
        # Se autenticado, verificar se é dono
        playlist = crud.get_playlist(db, playlist_id, current_user.id)
    else:
        # Se não autenticado, buscar sem filtro de usuário
        playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    
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
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"Tentativa de deletar playlist {playlist_id} do usuário {current_user.id}")
    
    deleted = crud.delete_playlist(db, playlist_id, current_user.id)
    
    if not deleted:
        logger.warning(f"Playlist {playlist_id} não encontrada para usuário {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist não encontrada"
        )
    
    logger.info(f"Playlist {playlist_id} deletada com sucesso")
    return None



@router.get("/{playlist_id}/items", response_model=List[schemas.PlaylistItemOut])
def get_playlist_items(
    playlist_id: int,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    Lista todos os itens de uma playlist (público).
    """
    # Verificar se playlist existe
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
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
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"Tentativa de adicionar item à playlist {playlist_id}: {item.media_type} - {item.title}")

    playlist = crud.get_playlist(db, playlist_id, current_user.id)
    if not playlist:
        logger.warning(f"Playlist {playlist_id} não encontrada para usuário {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist não encontrada"
        )
    
    db_item = crud.upsert_playlist_item(db, playlist_id, item)
    logger.info(f"Item adicionado à playlist {playlist_id} com sucesso - ID: {db_item.id}")
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
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"Tentativa de remover item {item_id} da playlist {playlist_id}")

    playlist = crud.get_playlist(db, playlist_id, current_user.id)
    if not playlist:
        logger.warning(f"Playlist {playlist_id} não encontrada para usuário {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist não encontrada"
        )
    
    deleted = crud.delete_playlist_item(db, item_id, playlist_id)
    
    if not deleted:
        logger.warning(f"Item {item_id} não encontrado na playlist {playlist_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item não encontrado"
        )
    
    logger.info(f"Item {item_id} removido da playlist {playlist_id} com sucesso")
    return None



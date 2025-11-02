"""Operações CRUD."""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models import (
    User, Favorite, HistoryItem, Playlist, PlaylistItem,
    Tag, MediaTag, Setting, Statistics, MediaType
)
from app import schemas
from app.security import get_password_hash, verify_password


# ==================== USER CRUD ====================
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Busca usuário por email."""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: schemas.UserSignup) -> User:
    """Cria novo usuário."""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Autentica usuário."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# ==================== FAVORITE CRUD ====================
def get_favorite_by_uri(db: Session, user_id: int, media_uri: str, media_type: MediaType) -> Optional[Favorite]:
    """Busca favorito por URI e tipo."""
    return db.query(Favorite).filter(
        and_(
            Favorite.user_id == user_id,
            Favorite.media_uri == media_uri,
            Favorite.media_type == media_type
        )
    ).first()


def get_user_favorites(db: Session, user_id: int) -> List[Favorite]:
    """Lista todos os favoritos do usuário."""
    return db.query(Favorite).filter(Favorite.user_id == user_id).all()


def upsert_favorite(db: Session, user_id: int, favorite: schemas.FavoriteIn) -> Favorite:
    """Cria ou atualiza favorito (upsert)."""
    existing = get_favorite_by_uri(db, user_id, favorite.media_uri, favorite.media_type)
    
    if existing:
        # Atualiza existente
        existing.title = favorite.title
        existing.mime_type = favorite.mime_type
        existing.duration_ms = favorite.duration_ms
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Cria novo
        db_favorite = Favorite(
            user_id=user_id,
            **favorite.dict()
        )
        db.add(db_favorite)
        db.commit()
        db.refresh(db_favorite)
        return db_favorite


def delete_favorite_by_uri(db: Session, user_id: int, media_uri: str, media_type: MediaType) -> bool:
    """Deleta favorito por URI e tipo."""
    favorite = get_favorite_by_uri(db, user_id, media_uri, media_type)
    if favorite:
        db.delete(favorite)
        db.commit()
        return True
    return False


# ==================== HISTORY CRUD ====================
def get_history_item_by_uri(db: Session, user_id: int, media_uri: str, media_type: MediaType) -> Optional[HistoryItem]:
    """Busca item de histórico por URI e tipo."""
    return db.query(HistoryItem).filter(
        and_(
            HistoryItem.user_id == user_id,
            HistoryItem.media_uri == media_uri,
            HistoryItem.media_type == media_type
        )
    ).first()


def get_user_history(db: Session, user_id: int) -> List[HistoryItem]:
    """Lista todo o histórico do usuário."""
    return db.query(HistoryItem).filter(HistoryItem.user_id == user_id).all()


def upsert_history_item(db: Session, user_id: int, history_item: schemas.HistoryItemIn) -> HistoryItem:
    """Cria ou atualiza item de histórico (upsert)."""
    existing = get_history_item_by_uri(db, user_id, history_item.media_uri, history_item.media_type)
    
    if existing:
        # Atualiza existente
        existing.title = history_item.title
        existing.mime_type = history_item.mime_type
        existing.duration_ms = history_item.duration_ms
        existing.last_position_ms = history_item.last_position_ms
        existing.play_count += 1  # Incrementa contador
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Cria novo
        db_history = HistoryItem(
            user_id=user_id,
            **history_item.dict()
        )
        db.add(db_history)
        db.commit()
        db.refresh(db_history)
        return db_history


# ==================== PLAYLIST CRUD ====================
def get_playlist(db: Session, playlist_id: int, user_id: int) -> Optional[Playlist]:
    """Busca playlist por ID."""
    return db.query(Playlist).filter(
        and_(
            Playlist.id == playlist_id,
            Playlist.user_id == user_id
        )
    ).first()


def get_user_playlists(db: Session, user_id: int) -> List[Playlist]:
    """Lista todas as playlists do usuário."""
    return db.query(Playlist).filter(Playlist.user_id == user_id).all()


def create_playlist(db: Session, user_id: int, playlist: schemas.PlaylistIn) -> Playlist:
    """Cria nova playlist."""
    db_playlist = Playlist(
        user_id=user_id,
        **playlist.dict()
    )
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist


def update_playlist(db: Session, playlist_id: int, user_id: int, playlist: schemas.PlaylistIn) -> Optional[Playlist]:
    """Atualiza playlist existente."""
    db_playlist = get_playlist(db, playlist_id, user_id)
    if not db_playlist:
        return None
    
    db_playlist.name = playlist.name
    db_playlist.description = playlist.description
    db.commit()
    db.refresh(db_playlist)
    return db_playlist


def delete_playlist(db: Session, playlist_id: int, user_id: int) -> bool:
    """Deleta playlist."""
    playlist = get_playlist(db, playlist_id, user_id)
    if playlist:
        db.delete(playlist)
        db.commit()
        return True
    return False


# ==================== PLAYLIST ITEM CRUD ====================
def get_playlist_item(db: Session, item_id: int, playlist_id: int) -> Optional[PlaylistItem]:
    """Busca item de playlist por ID."""
    return db.query(PlaylistItem).filter(
        and_(
            PlaylistItem.id == item_id,
            PlaylistItem.playlist_id == playlist_id
        )
    ).first()


def get_playlist_items(db: Session, playlist_id: int) -> List[PlaylistItem]:
    """Lista todos os itens de uma playlist."""
    return db.query(PlaylistItem).filter(PlaylistItem.playlist_id == playlist_id).all()


def upsert_playlist_item(db: Session, playlist_id: int, item: schemas.PlaylistItemIn) -> PlaylistItem:
    """Cria ou atualiza item de playlist (upsert)."""
    existing = db.query(PlaylistItem).filter(
        and_(
            PlaylistItem.playlist_id == playlist_id,
            PlaylistItem.media_uri == item.media_uri,
            PlaylistItem.media_type == item.media_type
        )
    ).first()
    
    if existing:
        # Atualiza existente
        existing.title = item.title
        existing.mime_type = item.mime_type
        existing.duration_ms = item.duration_ms
        existing.position = item.position
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Cria novo
        db_item = PlaylistItem(
            playlist_id=playlist_id,
            **item.dict()
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item


def delete_playlist_item(db: Session, item_id: int, playlist_id: int) -> bool:
    """Deleta item de playlist."""
    item = get_playlist_item(db, item_id, playlist_id)
    if item:
        db.delete(item)
        db.commit()
        return True
    return False


# ==================== TAG CRUD ====================
def get_tag(db: Session, tag_id: int, user_id: int) -> Optional[Tag]:
    """Busca tag por ID."""
    return db.query(Tag).filter(
        and_(
            Tag.id == tag_id,
            Tag.user_id == user_id
        )
    ).first()


def get_user_tags(db: Session, user_id: int) -> List[Tag]:
    """Lista todas as tags do usuário."""
    return db.query(Tag).filter(Tag.user_id == user_id).all()


def create_tag(db: Session, user_id: int, tag: schemas.TagIn) -> Tag:
    """Cria nova tag."""
    db_tag = Tag(
        user_id=user_id,
        **tag.dict()
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, tag_id: int, user_id: int) -> bool:
    """Deleta tag."""
    tag = get_tag(db, tag_id, user_id)
    if tag:
        db.delete(tag)
        db.commit()
        return True
    return False


# ==================== MEDIA TAG CRUD ====================
def get_media_tag(db: Session, media_uri: str, media_type: MediaType, tag_id: int) -> Optional[MediaTag]:
    """Busca vínculo tag-mídia."""
    return db.query(MediaTag).filter(
        and_(
            MediaTag.media_uri == media_uri,
            MediaTag.media_type == media_type,
            MediaTag.tag_id == tag_id
        )
    ).first()


def create_media_tag(db: Session, media_tag: schemas.MediaTagIn) -> MediaTag:
    """Cria vínculo tag-mídia."""
    existing = get_media_tag(db, media_tag.media_uri, media_tag.media_type, media_tag.tag_id)
    if existing:
        return existing
    
    db_media_tag = MediaTag(**media_tag.dict())
    db.add(db_media_tag)
    db.commit()
    db.refresh(db_media_tag)
    return db_media_tag


def delete_media_tag(db: Session, media_tag_id: int) -> bool:
    """Deleta vínculo tag-mídia."""
    media_tag = db.query(MediaTag).filter(MediaTag.id == media_tag_id).first()
    if media_tag:
        db.delete(media_tag)
        db.commit()
        return True
    return False


# ==================== SETTINGS CRUD ====================
def get_user_settings(db: Session, user_id: int) -> Optional[Setting]:
    """Busca configurações do usuário."""
    return db.query(Setting).filter(Setting.user_id == user_id).first()


def create_default_settings(db: Session, user_id: int) -> Setting:
    """Cria configurações padrão para o usuário."""
    db_settings = Setting(user_id=user_id)
    db.add(db_settings)
    db.commit()
    db.refresh(db_settings)
    return db_settings


def upsert_settings(db: Session, user_id: int, settings: schemas.SettingsIn) -> Setting:
    """Cria ou atualiza configurações do usuário."""
    existing = get_user_settings(db, user_id)
    
    if existing:
        existing.theme_mode = settings.theme_mode
        existing.playback_speed = settings.playback_speed
        existing.auto_resume = settings.auto_resume
        db.commit()
        db.refresh(existing)
        return existing
    else:
        db_settings = Setting(
            user_id=user_id,
            **settings.dict()
        )
        db.add(db_settings)
        db.commit()
        db.refresh(db_settings)
        return db_settings


# ==================== STATISTICS CRUD ====================
def get_user_statistics(db: Session, user_id: int) -> Optional[Statistics]:
    """Busca estatísticas do usuário."""
    return db.query(Statistics).filter(Statistics.user_id == user_id).first()


def create_default_statistics(db: Session, user_id: int) -> Statistics:
    """Cria estatísticas padrão para o usuário."""
    db_stats = Statistics(user_id=user_id)
    db.add(db_stats)
    db.commit()
    db.refresh(db_stats)
    return db_stats


def upsert_statistics(db: Session, user_id: int, statistics: schemas.StatisticsIn) -> Statistics:
    """Cria ou atualiza estatísticas do usuário."""
    existing = get_user_statistics(db, user_id)
    
    if existing:
        existing.total_play_count = statistics.total_play_count
        existing.total_listen_time_ms = statistics.total_listen_time_ms
        existing.favorite_count = statistics.favorite_count
        existing.playlist_count = statistics.playlist_count
        db.commit()
        db.refresh(existing)
        return existing
    else:
        db_stats = Statistics(
            user_id=user_id,
            **statistics.dict()
        )
        db.add(db_stats)
        db.commit()
        db.refresh(db_stats)
        return db_stats



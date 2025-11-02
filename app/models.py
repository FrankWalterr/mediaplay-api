"""Modelos SQLAlchemy do banco de dados."""
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db import Base


class MediaType(str, enum.Enum):
    """Tipo de mídia."""
    AUDIO = "audio"
    VIDEO = "video"


# Modelo base com timestamps
class TimestampMixin:
    """Mixin para adicionar created_at e updated_at."""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(Base, TimestampMixin):
    """Modelo de usuário."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Relacionamentos
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    history = relationship("HistoryItem", back_populates="user", cascade="all, delete-orphan")
    playlists = relationship("Playlist", back_populates="user", cascade="all, delete-orphan")
    settings = relationship("Setting", back_populates="user", cascade="all, delete-orphan", uselist=False)


class Favorite(Base, TimestampMixin):
    """Modelo de favorito."""
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Chave natural: media_uri + media_type
    media_uri = Column(String, nullable=False)
    media_type = Column(SQLEnum(MediaType), nullable=False)
    
    title = Column(String, nullable=False)
    mime_type = Column(String, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    
    # Relacionamentos
    user = relationship("User", back_populates="favorites")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'media_uri', 'media_type', name='uq_favorite_user_media'),
    )


class HistoryItem(Base, TimestampMixin):
    """Modelo de item de histórico."""
    __tablename__ = "history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Chave natural: media_uri + media_type
    media_uri = Column(String, nullable=False)
    media_type = Column(SQLEnum(MediaType), nullable=False)
    
    title = Column(String, nullable=False)
    mime_type = Column(String, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    last_position_ms = Column(Integer, default=0, nullable=False)
    last_played = Column(DateTime, default=datetime.utcnow, nullable=False)
    play_count = Column(Integer, default=1, nullable=False)
    
    # Relacionamentos
    user = relationship("User", back_populates="history")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'media_uri', 'media_type', name='uq_history_user_media'),
    )


class Playlist(Base, TimestampMixin):
    """Modelo de playlist."""
    __tablename__ = "playlists"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    # Relacionamentos
    user = relationship("User", back_populates="playlists")
    items = relationship("PlaylistItem", back_populates="playlist", cascade="all, delete-orphan", order_by="PlaylistItem.position")


class PlaylistItem(Base, TimestampMixin):
    """Modelo de item de playlist."""
    __tablename__ = "playlist_items"
    
    id = Column(Integer, primary_key=True, index=True)
    playlist_id = Column(Integer, ForeignKey("playlists.id", ondelete="CASCADE"), nullable=False)
    
    # Chave natural: playlist_id + media_uri + media_type
    media_uri = Column(String, nullable=False)
    media_type = Column(SQLEnum(MediaType), nullable=False)
    
    title = Column(String, nullable=False)
    mime_type = Column(String, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    position = Column(Integer, nullable=False)  # Ordem na playlist
    
    # Relacionamentos
    playlist = relationship("Playlist", back_populates="items")
    
    __table_args__ = (
        UniqueConstraint('playlist_id', 'media_uri', 'media_type', name='uq_playlist_item_media'),
    )


class Tag(Base, TimestampMixin):
    """Modelo de tag."""
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String, nullable=False)
    color = Column(String, nullable=True)  # Cor da tag em hex
    
    # Relacionamentos
    media_tags = relationship("MediaTag", back_populates="tag", cascade="all, delete-orphan")


class MediaTag(Base, TimestampMixin):
    """Modelo de vínculo tag-mídia."""
    __tablename__ = "media_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), nullable=False)
    
    # Chave natural: media_uri + media_type + tag_id
    media_uri = Column(String, nullable=False)
    media_type = Column(SQLEnum(MediaType), nullable=False)
    
    # Relacionamentos
    tag = relationship("Tag", back_populates="media_tags")
    
    __table_args__ = (
        UniqueConstraint('tag_id', 'media_uri', 'media_type', name='uq_media_tag'),
    )


class Setting(Base, TimestampMixin):
    """Modelo de configurações do usuário."""
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    theme_mode = Column(String, default="light", nullable=False)  # light, dark, auto
    playback_speed = Column(Float, default=1.0, nullable=False)
    auto_resume = Column(Integer, default=0, nullable=False)  # 0 ou 1 (boolean)
    
    # Relacionamentos
    user = relationship("User", back_populates="settings")


class Statistics(Base, TimestampMixin):
    """Modelo de estatísticas do usuário."""
    __tablename__ = "statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    total_play_count = Column(Integer, default=0, nullable=False)
    total_listen_time_ms = Column(Integer, default=0, nullable=False)
    favorite_count = Column(Integer, default=0, nullable=False)
    playlist_count = Column(Integer, default=0, nullable=False)


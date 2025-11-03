"""Modelos SQLAlchemy do banco de dados."""
from __future__ import annotations
from datetime import datetime
from typing import Optional
import enum

from sqlalchemy import String, DateTime, Float, ForeignKey, Text, Enum as SQLEnum, UniqueConstraint, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class MediaType(str, enum.Enum):
    """Tipo de mídia."""
    AUDIO = "audio"
    VIDEO = "video"


# Modelo base com timestamps
class TimestampMixin:
    """Mixin para adicionar created_at e updated_at."""
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(Base, TimestampMixin):
    """Modelo de usuário."""
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    
    # Relacionamentos
    favorites: Mapped[list["Favorite"]] = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    history: Mapped[list["HistoryItem"]] = relationship("HistoryItem", back_populates="user", cascade="all, delete-orphan")
    playlists: Mapped[list["Playlist"]] = relationship("Playlist", back_populates="user", cascade="all, delete-orphan")
    settings: Mapped[Optional["Setting"]] = relationship("Setting", back_populates="user", cascade="all, delete-orphan", uselist=False)


class Favorite(Base, TimestampMixin):
    """Modelo de favorito."""
    __tablename__ = "favorites"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Chave natural: media_uri + media_type
    media_uri: Mapped[str] = mapped_column(String, nullable=False)
    media_type: Mapped[MediaType] = mapped_column(SQLEnum(MediaType), nullable=False)
    
    title: Mapped[str] = mapped_column(String, nullable=False)
    mime_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Relacionamentos
    user: Mapped["User"] = relationship("User", back_populates="favorites")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'media_uri', 'media_type', name='uq_favorite_user_media'),
    )


class HistoryItem(Base, TimestampMixin):
    """Modelo de item de histórico."""
    __tablename__ = "history"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Chave natural: media_uri + media_type
    media_uri: Mapped[str] = mapped_column(String, nullable=False)
    media_type: Mapped[MediaType] = mapped_column(SQLEnum(MediaType), nullable=False)
    
    title: Mapped[str] = mapped_column(String, nullable=False)
    mime_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    last_position_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_played: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    play_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    
    # Relacionamentos
    user: Mapped["User"] = relationship("User", back_populates="history")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'media_uri', 'media_type', name='uq_history_user_media'),
    )


class Playlist(Base, TimestampMixin):
    """Modelo de playlist."""
    __tablename__ = "playlists"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relacionamentos
    user: Mapped["User"] = relationship("User", back_populates="playlists")
    items: Mapped[list["PlaylistItem"]] = relationship("PlaylistItem", back_populates="playlist", cascade="all, delete-orphan", order_by="PlaylistItem.position")


class PlaylistItem(Base, TimestampMixin):
    """Modelo de item de playlist."""
    __tablename__ = "playlist_items"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    playlist_id: Mapped[int] = mapped_column(Integer, ForeignKey("playlists.id", ondelete="CASCADE"), nullable=False)
    
    # Chave natural: playlist_id + media_uri + media_type
    media_uri: Mapped[str] = mapped_column(String, nullable=False)
    media_type: Mapped[MediaType] = mapped_column(SQLEnum(MediaType), nullable=False)
    
    title: Mapped[str] = mapped_column(String, nullable=False)
    mime_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)  # Ordem na playlist
    
    # Relacionamentos
    playlist: Mapped["Playlist"] = relationship("Playlist", back_populates="items")
    
    __table_args__ = (
        UniqueConstraint('playlist_id', 'media_uri', 'media_type', name='uq_playlist_item_media'),
    )


class Tag(Base, TimestampMixin):
    """Modelo de tag."""
    __tablename__ = "tags"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    name: Mapped[str] = mapped_column(String, nullable=False)
    color: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Cor da tag em hex
    
    # Relacionamentos
    media_tags: Mapped[list["MediaTag"]] = relationship("MediaTag", back_populates="tag", cascade="all, delete-orphan")


class MediaTag(Base, TimestampMixin):
    """Modelo de vínculo tag-mídia."""
    __tablename__ = "media_tags"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), nullable=False)
    
    # Chave natural: media_uri + media_type + tag_id
    media_uri: Mapped[str] = mapped_column(String, nullable=False)
    media_type: Mapped[MediaType] = mapped_column(SQLEnum(MediaType), nullable=False)
    
    # Relacionamentos
    tag: Mapped["Tag"] = relationship("Tag", back_populates="media_tags")
    
    __table_args__ = (
        UniqueConstraint('tag_id', 'media_uri', 'media_type', name='uq_media_tag'),
    )


class Setting(Base, TimestampMixin):
    """Modelo de configurações do usuário."""
    __tablename__ = "settings"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    theme_mode: Mapped[str] = mapped_column(String, default="light", nullable=False)  # light, dark, auto
    playback_speed: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    auto_resume: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # 0 ou 1 (boolean)
    
    # Relacionamentos
    user: Mapped["User"] = relationship("User", back_populates="settings")


class Statistics(Base, TimestampMixin):
    """Modelo de estatísticas do usuário."""
    __tablename__ = "statistics"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    total_play_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_listen_time_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    favorite_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    playlist_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

"""Schemas Pydantic para validação e serialização."""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models import MediaType


# Auth Schemas
class UserSignup(BaseModel):
    """Schema de registro de usuário."""
    email: EmailStr
    name: str
    password: str


class UserSignin(BaseModel):
    """Schema de login de usuário."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema de resposta de token JWT."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema de dados do token."""
    user_id: Optional[int] = None
    email: Optional[str] = None


# User Schema
class UserOut(BaseModel):
    """Schema de saída do usuário."""
    id: int
    email: str
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Favorite Schemas
class FavoriteBase(BaseModel):
    """Schema base de favorito."""
    media_uri: str
    media_type: MediaType
    title: str
    mime_type: Optional[str] = None
    duration_ms: Optional[int] = None


class FavoriteIn(FavoriteBase):
    """Schema de entrada de favorito."""
    pass


class FavoriteOut(FavoriteBase):
    """Schema de saída de favorito."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# History Schemas
class HistoryItemBase(BaseModel):
    """Schema base de item de histórico."""
    media_uri: str
    media_type: MediaType
    title: str
    mime_type: Optional[str] = None
    duration_ms: Optional[int] = None
    last_position_ms: int = 0
    play_count: int = 1


class HistoryItemIn(HistoryItemBase):
    """Schema de entrada de item de histórico."""
    pass


class HistoryItemOut(HistoryItemBase):
    """Schema de saída de item de histórico."""
    id: int
    user_id: int
    last_played: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Playlist Schemas
class PlaylistBase(BaseModel):
    """Schema base de playlist."""
    name: str
    description: Optional[str] = None


class PlaylistIn(PlaylistBase):
    """Schema de entrada de playlist."""
    pass


class PlaylistOut(PlaylistBase):
    """Schema de saída de playlist."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PlaylistWithItems(PlaylistOut):
    """Schema de playlist com itens."""
    items: list["PlaylistItemOut"] = []
    
    class Config:
        from_attributes = True


class PlaylistItemBase(BaseModel):
    """Schema base de item de playlist."""
    media_uri: str
    media_type: MediaType
    title: str
    mime_type: Optional[str] = None
    duration_ms: Optional[int] = None
    position: int


class PlaylistItemIn(PlaylistItemBase):
    """Schema de entrada de item de playlist."""
    pass


class PlaylistItemOut(PlaylistItemBase):
    """Schema de saída de item de playlist."""
    id: int
    playlist_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Tag Schemas
class TagBase(BaseModel):
    """Schema base de tag."""
    name: str
    color: Optional[str] = None


class TagIn(TagBase):
    """Schema de entrada de tag."""
    pass


class TagOut(TagBase):
    """Schema de saída de tag."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MediaTagBase(BaseModel):
    """Schema base de vínculo tag-mídia."""
    tag_id: int
    media_uri: str
    media_type: MediaType


class MediaTagIn(MediaTagBase):
    """Schema de entrada de vínculo tag-mídia."""
    pass


class MediaTagOut(MediaTagBase):
    """Schema de saída de vínculo tag-mídia."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Settings Schema
class SettingsBase(BaseModel):
    """Schema base de configurações."""
    theme_mode: str = "light"
    playback_speed: float = 1.0
    auto_resume: int = 0


class SettingsIn(SettingsBase):
    """Schema de entrada de configurações."""
    pass


class SettingsOut(SettingsBase):
    """Schema de saída de configurações."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Statistics Schema
class StatisticsBase(BaseModel):
    """Schema base de estatísticas."""
    total_play_count: int = 0
    total_listen_time_ms: int = 0
    favorite_count: int = 0
    playlist_count: int = 0


class StatisticsIn(StatisticsBase):
    """Schema de entrada de estatísticas."""
    pass


class StatisticsOut(StatisticsBase):
    """Schema de saída de estatísticas."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Health check
class Health(BaseModel):
    """Schema de health check."""
    status: str = "ok"
    version: str



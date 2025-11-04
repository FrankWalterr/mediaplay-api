# app/config.py
from __future__ import annotations
import os
from pydantic import BaseModel
from functools import lru_cache

class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL") or os.getenv("database_url", "")
    sql_echo: bool = os.getenv("SQL_ECHO", "false").lower() == "true"
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

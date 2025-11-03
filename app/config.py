# app/config.py
from __future__ import annotations
import os
from pydantic import BaseModel
from functools import lru_cache

class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL") or os.getenv("database_url", "")
    sql_echo: bool = os.getenv("SQL_ECHO", "false").lower() == "true"

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

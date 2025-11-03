# app/routers/debug.py
from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import get_db

router = APIRouter(prefix="/debug", tags=["debug"])

@router.get("/db")
def db_health(db: Session = Depends(get_db)) -> dict[str, str]:
    # Testa round-trip ao banco
    db.execute(text("SELECT 1"))
    return {"db": "ok"}

@router.get("/smoke")
def smoke(db: Session = Depends(get_db)) -> dict[str, str]:
    # Acrescente aqui outros checks que façam sentido
    db.execute(text("SELECT 1"))
    return {
        "app": "ok",
        "db": "ok",
        "version": "v1",  # opcional: injete git sha
    }

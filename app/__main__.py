# app/main.py
from __future__ import annotations

from fastapi import FastAPI
from app.db import init_db

app = FastAPI(title="Mediaplay API")

@app.on_event("startup")
def on_startup() -> None:
    # Inicializa/verifica o banco ao subir a aplicação
    init_db()

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

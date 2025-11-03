# app/db.py
"""
Camada de acesso a dados (SQLAlchemy) para a API Mediaplay.

- Normaliza URLs do Render (postgres:// → postgresql+psycopg://).
- Cria o Engine com pool_pre_ping (evita conexões zumbis).
- Controla echo de SQL via settings.sql_echo.
- Expõe SessionLocal, dependência get_db e a função init_db().
"""

from __future__ import annotations

import logging
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings  # precisa existir (ver exemplo de config abaixo)

try:
    from app.models import Base  # Base declarativa dos seus modelos
except Exception:
    Base = None  # type: ignore

log = logging.getLogger(__name__)


def _normalize(url: str) -> str:
    """
    Render às vezes fornece 'postgres://...', mas SQLAlchemy 2.x
    requer 'postgresql+psycopg://...'.
    """
    if not url:
        raise ValueError("Config 'database_url' indefinida (ver app.config.Settings).")
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    return url


SQLALCHEMY_DATABASE_URL = _normalize(settings.database_url)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    echo=getattr(settings, "sql_echo", False),
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator:
    """
    Dependência FastAPI: injeta uma sessão por request.
        def endpoint(db: Session = Depends(get_db)): ...
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """
    Inicializa/verifica o schema de banco em tempo de execução.
    Idempotente: se as tabelas já existem, não recria.
    """
    if Base is None:
        log.warning("Base não encontrada; init_db não executará create_all (ok se usar Alembic).")
        return
    try:
        Base.metadata.create_all(bind=engine)
        log.info("Tabelas verificadas/criadas com Base.metadata.create_all.")
    except Exception as e:
        log.exception("Falha no init_db/create_all: %s", e)
        raise

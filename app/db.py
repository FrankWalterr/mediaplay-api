# app/db.py
"""
Camada de acesso a dados (SQLAlchemy) para a API Mediaplay.

- Normaliza URLs do Render (postgres:// → postgresql+psycopg://).
- Cria o Engine com pool_pre_ping (evita conexões zumbis).
- Exibe SQL no log (echo=True) durante validação; pode desligar em produção.
- Expõe SessionLocal e dependência get_db para uso nos endpoints.
- (Opcional) cria tabelas automaticamente se Base estiver disponível.
"""

from __future__ import annotations

import logging
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings  

try:
    from app.models import Base  
except Exception:  
    Base = None  

log = logging.getLogger(__name__)


def _normalize(url: str) -> str:
    """
    Render frequentemente fornece 'postgres://...' mas SQLAlchemy 2.x
    requer 'postgresql+psycopg://...'. Esta função ajusta o prefixo.
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
    echo=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator:
    """
    Dependência FastAPI: injeta uma sessão por request.
    Uso:
        def endpoint(db: Session = Depends(get_db)):
            ...
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


try:
    if Base is not None:
        Base.metadata.create_all(bind=engine)
        log.info("Base metadata criada (create_all).")
    else:
        log.warning("Base não encontrada; pulando create_all (ok se usar Alembic).")
except Exception as e:
    log.warning("Falha ao executar Base.metadata.create_all: %s", e)

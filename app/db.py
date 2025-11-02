"""Configuração do banco de dados."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Criar engine do banco
if settings.database_url.startswith("sqlite"):
    # SQLite local
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        echo=settings.echo_sql,
    )
else:
    # PostgreSQL em produção
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=settings.pool_pre_ping,
        pool_size=settings.pool_size,
        max_overflow=settings.max_overflow,
        echo=settings.echo_sql,
    )

# Sessão do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()


def get_db():
    """Dependency para obter sessão do banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Cria todas as tabelas no banco de dados."""
    Base.metadata.create_all(bind=engine)



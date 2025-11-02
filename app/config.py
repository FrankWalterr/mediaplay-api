"""Configurações da aplicação."""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Configurações do aplicativo."""
    
    # Nome da aplicação
    app_name: str = "Mediaplay API"
    app_version: str = "1.0.0"
    
    # Segurança
    secret_key: str = "your-secret-key-change-in-production-use-openssl-rand-hex-32"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    cors_origins: List[str] = ["*"]  # Em produção, especificar domínios exatos
    
    # Database
    database_url: str = "sqlite:///./mediaplay.db"  # Local: SQLite
    
    # Para produção com PostgreSQL no Render:
    # database_url: str = "postgresql://user:password@host:5432/dbname"
    
    # Configurações do SQLAlchemy
    echo_sql: bool = False
    pool_pre_ping: bool = True
    pool_size: int = 5
    max_overflow: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instância global de configurações
settings = Settings()


"""Módulo de segurança: JWT e hash de senhas."""
from datetime import datetime, timedelta
from typing import Optional
import jwt
import hashlib
import secrets
from app.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha plain corresponde ao hash."""
    # Extrair salt e hash do formato "salt:hash"
    try:
        salt, stored_hash = hashed_password.split(':', 1)
        new_hash = hashlib.sha256((plain_password + salt).encode()).hexdigest()
        return new_hash == stored_hash
    except ValueError:
        return False


def get_password_hash(password: str) -> str:
    """Gera hash SHA256 da senha com salt."""
    # Gerar salt aleatório
    salt = secrets.token_hex(16)
    # Hash da senha + salt
    hash_value = hashlib.sha256((password + salt).encode()).hexdigest()
    # Retornar no formato "salt:hash"
    return f"{salt}:{hash_value}"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decodifica JWT access token."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


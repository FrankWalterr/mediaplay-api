"""Router de autenticação."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db import get_db
from app import schemas, crud
from app.security import create_access_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=schemas.Token)
def signup(user: schemas.UserSignup, db: Session = Depends(get_db)):
    """
    Registra novo usuário.
    
    Retorna JWT token para autenticação subsequente.
    """
    # Verifica se email já existe
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado"
        )
    
    # Cria usuário
    new_user = crud.create_user(db, user)
    
    # Cria configurações padrão e estatísticas
    crud.create_default_settings(db, new_user.id)
    crud.create_default_statistics(db, new_user.id)
    
    # Gera token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"user_id": new_user.id, "email": new_user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signin", response_model=schemas.Token)
def signin(credentials: schemas.UserSignin, db: Session = Depends(get_db)):
    """
    Autentica usuário existente.
    
    Retorna JWT token para autenticação subsequente.
    """
    user = crud.authenticate_user(db, credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Gera token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


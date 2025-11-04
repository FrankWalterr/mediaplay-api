from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta

from app import schemas, crud
from app.db import get_db
from app.security import create_access_token, verify_password
from app.models import User

router = APIRouter()

@router.post("/signup", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
def signup(user_data: schemas.UserSignup, db: Session = Depends(get_db)):
    """Cria um novo usuário e retorna token JWT."""
    # Verificar se usuário já existe
    existing_user = crud.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Criar usuário
    new_user = crud.create_user(db, user_data)
    
    # Criar settings e statistics padrão
    try:
        crud.create_default_settings(db, new_user.id)
        crud.create_default_statistics(db, new_user.id)
    except Exception as e:
        # Log do erro mas continua
        pass
    
    # Criar token JWT
    access_token = create_access_token(
        data={"user_id": new_user.id, "email": new_user.email}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/signin", response_model=schemas.Token)
def signin(credentials: schemas.UserSignin, db: Session = Depends(get_db)):
    """Autentica usuário e retorna token JWT."""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"Tentativa de login para email: {credentials.email}")
    
    # Verificar se usuário existe
    user = crud.get_user_by_email(db, credentials.email)
    if not user:
        logger.warning(f"Usuário não encontrado: {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info(f"Usuário encontrado: ID {user.id}, email {user.email}")
    
    # Autenticar usuário
    is_valid = crud.authenticate_user(db, credentials.email, credentials.password)
    if not is_valid:
        logger.warning(f"Senha inválida para usuário: {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info(f"Login bem-sucedido para usuário ID {is_valid.id}")
    
    # Criar token JWT
    access_token = create_access_token(
        data={"user_id": is_valid.id, "email": is_valid.email}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

"""Teste direto do banco."""
from app.db import SessionLocal, init_db
from app import crud, schemas

# Garantir que o banco está criado
init_db()

# Criar sessão
db = SessionLocal()

try:
    print("Testando criacao de usuario...")
    
    # Criar usuário
    user_data = schemas.UserSignup(
        email="test@example.com",
        name="Test User",
        password="secret123"
    )
    
    # Verificar se já existe
    existing = crud.get_user_by_email(db, user_data.email)
    if existing:
        print("Usuario ja existe, deletando...")
        db.delete(existing)
        db.commit()
    
    print("Criando novo usuario...")
    new_user = crud.create_user(db, user_data)
    print(f"Usuario criado: {new_user.id} - {new_user.email}")
    
    # Criar settings
    print("Criando settings...")
    settings = crud.create_default_settings(db, new_user.id)
    print(f"Settings criado: ID {settings.id}")
    
    # Criar statistics
    print("Criando statistics...")
    stats = crud.create_default_statistics(db, new_user.id)
    print(f"Statistics criado: ID {stats.id}")
    
    print("\n✅ Todos os testes passaram!")
    
except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()

finally:
    db.close()




"""Script para executar a API com logs visíveis."""
import os
import sys
import uvicorn

# Define DATABASE_URL se não estiver definida
if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "sqlite:///./mediaplay.db"
    print("✅ DATABASE_URL definida como SQLite local")

# Inicializa o banco de dados
print("🗄️ Inicializando banco de dados...")
try:
    from app.db import init_db
    init_db()
    print("✅ Banco de dados inicializado com sucesso!")
except Exception as e:
    print(f"⚠️ Aviso ao inicializar banco: {e}")
    print("Continuando mesmo assim...")

# Executa a API
print("\n🚀 Iniciando servidor FastAPI...")
print("📝 Logs serão exibidos abaixo:\n")
print("=" * 60)
print("API disponível em:")
print("  - Local: http://127.0.0.1:8000")
print("  - Rede: http://10.174.99.188:8000")
print("Documentação: http://10.174.99.188:8000/docs")
print("Health check: http://10.174.99.188:8000/health")
print("=" * 60)
print()

if __name__ == "__main__":
    # Usar 0.0.0.0 para aceitar conexões de qualquer IP na rede local
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


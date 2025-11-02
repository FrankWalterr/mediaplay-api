"""Aplicação FastAPI principal."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings as app_config
from app.db import init_db
from app.routers import (
    auth, favorites, history, playlists, tags, settings as settings_router, statistics
)

# Criar app FastAPI
app = FastAPI(
    title=app_config.app_name,
    version=app_config.app_version,
    description="API mestre para sincronização de dados do app Mediaplay offline-first",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint de health check."""
    return {"status": "ok", "version": app_config.app_version}


# Incluir routers
app.include_router(auth.router)
app.include_router(favorites.router)
app.include_router(history.router)
app.include_router(playlists.router)
app.include_router(tags.router)
app.include_router(settings_router.router)
app.include_router(statistics.router)


@app.on_event("startup")
def startup_event():
    """Evento executado ao iniciar a aplicação."""
    # Criar tabelas no banco de dados
    init_db()
    print(f"{app_config.app_name} v{app_config.app_version} iniciada com sucesso!")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


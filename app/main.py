import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, favorites, playlists, debug, history, settings, statistics, tags

# Configurar logging para aparecer no Render
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Mediaplay API", version="0.1.0")

# CORS liberado para o front (Netlify/Expo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["default"])
def root():
    return {
        "name": "Mediaplay API",
        "version": "0.1.0",
        "status": "online"
    }

@app.get("/health", tags=["default"])
def health():
    logger.info("Health check realizado")
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    """Evento de startup - cria tabelas do banco."""
    logger.info("Mediaplay API iniciando...")
    try:
        from app.db import init_db
        init_db()
        logger.info("Banco de dados inicializado com sucesso!")
    except Exception as e:
        logger.exception(f"Erro ao inicializar banco de dados: {e}")
    
    logger.info("API pronta para receber requisicoes!")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para logar todas as requisições."""
    logger.info(f"REQUEST: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"RESPONSE: {request.method} {request.url.path} - Status: {response.status_code}")
    return response

# Inclui rotas esperadas pelo frontend
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(playlists.router, prefix="/playlists", tags=["playlists"])
app.include_router(favorites.router, prefix="/favorites", tags=["favorites"])
app.include_router(history.router, tags=["history"])
app.include_router(settings.router, tags=["settings"])
app.include_router(statistics.router, tags=["statistics"])
app.include_router(tags.router, tags=["tags"])

# Rotas de debug
app.include_router(debug.router, tags=["debug"])

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, favorites, playlists, debug

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
    return {"status": "ok"}

# Inclui rotas esperadas pelo frontend
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(playlists.router, prefix="/playlists", tags=["playlists"])
app.include_router(favorites.router, prefix="/favorites", tags=["favorites"])

# Rotas de debug
app.include_router(debug.router, tags=["debug"])

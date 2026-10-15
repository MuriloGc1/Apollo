from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import Base, engine
from app.routers import auth, usuario, avisos, disciplinas, tarefas, notas, biblioteca, agenda, mensagens

Base.metadata.create_all(bind=engine)

app = FastAPI(title="APOLLO API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_lista,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for roteador in (auth.router, usuario.router, avisos.router, disciplinas.router, tarefas.router, notas.router, biblioteca.router, agenda.router, mensagens.router):
    app.include_router(roteador)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

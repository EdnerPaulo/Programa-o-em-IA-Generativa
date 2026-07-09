from fastapi import FastAPI
from app.api.v1.endpoints import recommendations
from app.db.session import init_db

app = FastAPI(title="BookMind IA - API Literária", version="1.0.0")

@app.on_event("startup")
def on_startup():
    try:
        init_db()
    except Exception:
        pass # Ignora caso o banco de dados não esteja conectado localmente ainda

app.include_router(recommendations.router, prefix="/api/v1")
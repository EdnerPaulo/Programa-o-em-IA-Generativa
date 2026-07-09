from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.api.v1.endpoints import auth, documents
from app.db.session import init_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LeitorIA")

app = FastAPI(title="Leitor IA API Backend", version="1.0.0")

@app.on_event("startup")
def on_startup():
    init_db()

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erro Crítico: {str(exc)}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Erro interno no servidor."})

app.include_router(auth.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
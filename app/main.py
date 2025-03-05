from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import auth, documents, queries
import logging

# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando la aplicación...")
    yield
    logger.info("Apagando la aplicación...")

app = FastAPI(lifespan=lifespan)

# Registrar rutas
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(queries.router, prefix="/queries", tags=["queries"])

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de IA con RAG y FAISS"}

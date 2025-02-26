from fastapi import FastAPI
from app.routes import auth, documents, queries


app = FastAPI()

# Registrar rutas
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(queries.router, prefix="/queries", tags=["queries"])

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de IA con RAG y FAISS"}

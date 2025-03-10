from fastapi import APIRouter, Depends, HTTPException, status
from ..models.user import User
from ..models.document import Query
from ..utils.auth import get_current_user
from ..utils.embeddings import get_embedding
from ..utils.database import mongo_db
import faiss
import numpy as np
import requests
from config.settings import settings
import logging

# Configura el logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Inicializar FAISS (debe ser el mismo índice que en pdfs.py)
dimension = 384
index = faiss.IndexFlatL2(dimension)

@router.post("/ask")
def ask_question(query: Query, current_user: User = Depends(get_current_user)):
    try:
        # Obtener el user_id del usuario autenticado
        user_id = current_user.id
        
        # Convertir la pregunta en un embedding
        query_embedding = get_embedding(query.query_text).reshape(1, -1)
        
        # Buscar los fragmentos más relevantes en FAISS
        k = 5  # Número de fragmentos a recuperar
        distances, indices = index.search(query_embedding, k)
        
        # Mostrar los índices y distancias de los fragmentos encontrados
        logger.info(f"Índices encontrados en FAISS: {indices}")
        logger.info(f"Distancias en FAISS: {distances}")
        
        # Recuperar los fragmentos de MongoDB
        fragment_ids = [int(idx) for idx in indices[0] if int(idx) >= 0]
        fragments = list(mongo_db.documents.find({"id": {"$in": fragment_ids}}))
        
        # Mostrar los fragmentos recuperados
        logger.info(f"Fragmentos recuperados de MongoDB: {fragments}")
        
        # Si no se encontraron fragmentos relevantes
        if not fragments:
            return {"answer": "No se encontró información relevante en los documentos.", "user_id": user_id}
        
        # Unir los fragmentos en un solo contexto
        context = " ".join([doc["text"] for doc in fragments])
        
        # Mostrar el contexto en los logs
        logger.info(f"Contexto enviado a Ollama: {context}")
        
        # Enviar a Ollama para generar la respuesta
        response = requests.post(
            f"{settings.OLLAMA_URL}/generate",
            json={"model": "llama3", "prompt": f"Context: {context}\nQuestion: {query.query_text}"}
        )
        
        return {"answer": response.json()["response"], "user_id": user_id}
    
    except Exception as e:
        logger.error(f"Error interno del servidor: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

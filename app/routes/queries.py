from fastapi import APIRouter, Depends, HTTPException
from app.utils.faiss_handler import query_document
from app.database.mongo_db import get_mongo_db
from app.utils.auth import get_current_user
from app.models.user import User
import ollama
import os
from redis import Redis

router = APIRouter()

# Configuración de Ollama y Redis
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
ollama.host = OLLAMA_HOST
redis_client = Redis(host="redis", port=6379, db=0, decode_responses=True)

@router.post("/query")
def query(query_text: str, db=Depends(get_mongo_db), current_user: User = Depends(get_current_user)):
    """Realiza una consulta en FAISS y genera respuestas con IA."""
    try:
        # Verificar si la consulta ya está en caché
        cache_key = f"query:{query_text}:{current_user.id}"
        cached_response = redis_client.get(cache_key)
        if cached_response:
            return {"answer": cached_response, "from_cache": True}

        # Buscar documentos relevantes en FAISS
        indices = query_document(query_text, top_k=5)

        # Obtener documentos del usuario desde MongoDB
        documents = db.documents.find({"user_id": current_user.id, "index_id": {"$in": indices}})
        context_docs = [doc["text"] for doc in documents if "text" in doc]

        if not context_docs:
            raise HTTPException(status_code=404, detail="No se encontraron documentos relevantes")

        # Construir el contexto
        context = "\n\n".join(context_docs)

        # Generar respuesta con Ollama
        response = ollama.generate(
            model="llama3",
            prompt=f"Contexto:\n{context}\n\nPregunta:\n{query_text}"
        )

        # Guardar la respuesta en caché por 1 hora
        redis_client.setex(cache_key, 3600, response["text"])

        return {"answer": response["text"], "context": context, "from_cache": False}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la consulta: {str(e)}")

import os
import logging
import numpy as np
import fitz
from sentence_transformers import SentenceTransformer
import faiss
from fastapi import HTTPException

logger = logging.getLogger(__name__)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
DIMENSION = 384

# Usar un índice más avanzado de FAISS
nlist = 100  # Número de clusters
quantizer = faiss.IndexFlatL2(DIMENSION)
index = faiss.IndexIVFFlat(quantizer, DIMENSION, nlist, faiss.METRIC_L2)
index.train(np.random.rand(1000, DIMENSION).astype("float32"))  # Entrenar el índice

def extract_text_from_pdf(file_path: str) -> str:
    """Extrae texto de un archivo PDF."""
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        doc.close()
        if not text.strip():
            raise ValueError("El PDF está vacío o no contiene texto")
        return text
    except Exception as e:
        logger.error(f"Error al extraer texto: {e}")
        raise ValueError(f"Error al extraer texto: {e}")

def extract_embeddings_from_text(text: str) -> list:
    """Genera embeddings a partir del texto."""
    try:
        embeddings = model.encode(text).tolist()
        return embeddings
    except Exception as e:
        logger.error(f"Error al generar embeddings: {e}")
        raise ValueError(f"Error al generar embeddings: {e}")

def query_document(query_text: str, top_k: int = 5) -> list:
    """Realiza una búsqueda en FAISS."""
    try:
        query_embedding = model.encode(query_text).astype("float32").reshape(1, -1)
        distances, indices = index.search(query_embedding, top_k)
        return indices.tolist()[0]
    except Exception as e:
        logger.error(f"Error en la búsqueda FAISS: {e}")
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {e}")

def index_document(file_path: str, db, user_id: int) -> str:
    """Indexa un documento en FAISS y MongoDB."""
    try:
        text = extract_text_from_pdf(file_path)
        embeddings = extract_embeddings_from_text(text)
        embeddings_array = np.array(embeddings, dtype="float32").reshape(1, -1)
        
        # Añadir al índice FAISS
        index.add(embeddings_array)
        index_id = index.ntotal - 1  # Último índice añadido
        
        # Guardar metadatos en MongoDB
        document_data = {
            "user_id": user_id,
            "filename": os.path.basename(file_path),
            "embeddings": embeddings.tolist(),
            "text": text,
            "index_id": index_id
        }
        result = db.documents.insert_one(document_data)
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Error al indexar documento: {e}")
        raise HTTPException(status_code=500, detail=f"Error al indexar: {e}")

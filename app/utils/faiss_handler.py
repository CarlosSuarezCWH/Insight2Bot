import os
import logging
import numpy as np
import fitz  # PyMuPDF para extracción de texto
from sentence_transformers import SentenceTransformer
import faiss
from fastapi import HTTPException

logger = logging.getLogger(__name__)

# Cargar modelo de embeddings
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
DIMENSION = model.get_sentence_embedding_dimension()

# Inicializar FAISS con un índice entrenable
nlist = 100  # Número de clusters para la estructura de FAISS
quantizer = faiss.IndexFlatL2(DIMENSION)
index = faiss.IndexIVFFlat(quantizer, DIMENSION, nlist, faiss.METRIC_L2)

# Se requiere entrenamiento antes de agregar datos
index_is_trained = False

def extract_text_from_pdf(file_path: str) -> str:
    """Extrae texto de un archivo PDF, asegurando calidad."""
    try:
        doc = fitz.open(file_path)
        text = "\n".join([page.get_text("text") for page in doc])
        doc.close()

        if not text.strip():
            raise ValueError("El PDF está vacío o no contiene texto extraíble.")

        return text
    except Exception as e:
        logger.error(f"Error al extraer texto: {e}")
        raise HTTPException(status_code=500, detail=f"Error al extraer texto: {e}")


def extract_embeddings_from_text(text: str) -> np.ndarray:
    """Convierte texto en embeddings usando un modelo preentrenado."""
    try:
        embeddings = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
        return embeddings.astype("float32")
    except Exception as e:
        logger.error(f"Error al generar embeddings: {e}")
        raise HTTPException(status_code=500, detail=f"Error al generar embeddings: {e}")


def train_index(data_samples: np.ndarray):
    """Entrena el índice FAISS si aún no ha sido entrenado."""
    global index_is_trained
    if not index_is_trained:
        index.train(data_samples)
        index_is_trained = True


def index_document(file_path: str, db, user_id: int) -> str:
    """Indexa un documento en FAISS y lo almacena en MongoDB."""
    try:
        text = extract_text_from_pdf(file_path)
        embeddings = extract_embeddings_from_text(text)

        # FAISS espera un formato (n, DIMENSION)
        embeddings = embeddings.reshape(1, -1)

        # Entrenar índice si es necesario
        if not index_is_trained:
            train_index(embeddings)

        # Agregar embeddings a FAISS
        index.add(embeddings)
        index_id = index.ntotal - 1  # Último índice añadido

        # Guardar metadatos en MongoDB
        document_data = {
            "user_id": user_id,
            "filename": os.path.basename(file_path),
            "text": text,
            "index_id": index_id
        }
        result = db.documents.insert_one(document_data)
        return str(result.inserted_id)

    except Exception as e:
        logger.error(f"Error al indexar documento: {e}")
        raise HTTPException(status_code=500, detail=f"Error al indexar: {e}")


def query_document(query_text: str, top_k: int = 5) -> list:
    """Realiza una consulta en FAISS y devuelve los índices más cercanos."""
    try:
        query_embedding = model.encode(query_text, convert_to_numpy=True, normalize_embeddings=True).astype("float32").reshape(1, -1)
        distances, indices = index.search(query_embedding, top_k)

        return indices.tolist()[0] if indices.size > 0 else []

    except Exception as e:
        logger.error(f"Error en la búsqueda FAISS: {e}")
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {e}")

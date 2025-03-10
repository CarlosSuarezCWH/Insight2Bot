from fastapi import APIRouter, UploadFile, Depends, HTTPException, status
from ..models.user import User
from ..utils.auth import get_current_user
from ..utils.embeddings import get_embedding
from ..utils.database import mongo_db
from ..models.document import Document
import faiss
import numpy as np
from pdfplumber import PDF
import re
import uuid
from datetime import datetime
import logging

# Configura el logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Inicializar FAISS
dimension = 384  # Dimensión de los embeddings generados por all-MiniLM-L6-v2
index = faiss.IndexFlatL2(dimension)

@router.post("/upload")
async def upload_pdf(file: UploadFile, current_user: User = Depends(get_current_user)):
    try:
        # Extraer texto del PDF
        text = ""
        with PDF.open(file.file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    # Preprocesamiento: eliminar espacios múltiples y saltos de línea
                    page_text = re.sub(r'\s+', ' ', page_text).strip()
                    text += page_text + " "
        
        # Mostrar el texto extraído en los logs
        logger.info(f"Texto extraído del PDF {file.filename}: {text}")
        
        # Dividir el texto en fragmentos
        fragments = [text[i:i + 500] for i in range(0, len(text), 500)]
        
        # Generar embeddings para cada fragmento y agregarlos al índice FAISS
        embeddings = np.array([get_embedding(fragment) for fragment in fragments])
        index.add(embeddings)
        
        # Guardar los fragmentos en MongoDB
        for fragment, embedding in zip(fragments, embeddings):
            doc = {
                "id": str(uuid.uuid4()),  # ID único
                "text": fragment,
                "embedding": embedding.tolist(),
                "filename": file.filename,
                "uploaded_by": current_user.id,
                "uploaded_at": datetime.utcnow()
            }
            mongo_db.documents.insert_one(doc)
        
        return {"filename": file.filename, "text": text[:100]}  # Devuelve el nombre del archivo y una muestra del texto
    
    except Exception as e:
        logger.error(f"Error al procesar el PDF: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al procesar el PDF: {str(e)}"
        )

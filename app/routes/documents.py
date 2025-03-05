from fastapi import APIRouter, UploadFile, Depends, HTTPException, File, BackgroundTasks
from sqlalchemy.orm import Session
from app.utils.faiss_handler import index_document
from app.database.mongo_db import get_mongo_db
from app.utils.auth import get_current_user
from app.models.user import User
import os
from app.config import Config
from celery import Celery

router = APIRouter()

# Configuración de Celery
celery_app = Celery("tasks", broker="redis://redis:6379/0")

@celery_app.task
def process_document_task(file_path: str, user_id: int):
    """Tarea en segundo plano para procesar documentos."""
    try:
        db = get_mongo_db()
        index_document(file_path, db, user_id)
        os.remove(file_path)  # Eliminamos el archivo temporal después de indexarlo
    except Exception as e:
        raise e

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Carga e indexa un documento PDF."""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    
    try:
        os.makedirs(Config.TEMP_PDF_PATH, exist_ok=True)
        file_path = os.path.join(Config.TEMP_PDF_PATH, f"{current_user.id}_{file.filename}")
        
        # Guardar el archivo
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # Procesar el documento en segundo plano con Celery
        process_document_task.delay(file_path, current_user.id)
        
        return {"message": "Documento recibido y en proceso de indexación"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el documento: {str(e)}")

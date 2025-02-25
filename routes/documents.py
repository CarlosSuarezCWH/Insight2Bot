from fastapi import APIRouter, UploadFile, Depends, HTTPException, File
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
def process_document(file_path: str, db, user_id: int):
    try:
        index_document(file_path, db, user_id)
    except Exception as e:
        raise e

@router.post("/upload", dependencies=[Depends(get_current_user)])
async def upload_document(file: UploadFile = File(...), db=Depends(get_mongo_db), current_user: User = Depends(get_current_user)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    
    try:
        os.makedirs(Config.TEMP_PDF_PATH, exist_ok=True)
        file_path = os.path.join(Config.TEMP_PDF_PATH, f"{current_user.id}_{file.filename}")
        
        # Guardar el archivo
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # Procesar el documento en segundo plano
        process_document.delay(file_path, db, current_user.id)
        
        return {"message": "Documento recibido y en proceso de indexación"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el documento: {str(e)}")

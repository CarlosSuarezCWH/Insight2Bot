from pydantic import BaseModel
from datetime import datetime

class DocumentCreate(BaseModel):
    filename: str
    user_id: int

class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    uploaded_at: datetime
    user_id: int

    class Config:
        from_attributes = True  # Habilita la compatibilidad con ORM (antes `orm_mode`)

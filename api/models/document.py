from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

class Document(BaseModel):
    id: Optional[str] = str(uuid.uuid4())  # ID único
    text: str
    embedding: List[float]
    filename: Optional[str]
    uploaded_by: Optional[str]
    uploaded_at: Optional[datetime]

    class Config:
        from_attributes = True  # Compatibilidad con Pydantic v2

class Query(BaseModel):
    query_text: str

    class Config:
        from_attributes = True

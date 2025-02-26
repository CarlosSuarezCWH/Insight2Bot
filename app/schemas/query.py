from pydantic import BaseModel
from datetime import datetime

class QueryCreate(BaseModel):
    document_id: str
    query: str
    user_id: int

class QueryResponse(BaseModel):
    query_id: str
    document_id: str
    query: str
    answer: str
    context: str
    timestamp: datetime
    user_id: int

    class Config:
        from_attributes = True  # Habilita la compatibilidad con ORM (antes `orm_mode`)

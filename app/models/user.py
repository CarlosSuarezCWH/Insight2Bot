from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))  # La contraseña se almacenará hasheada
    is_active = Column(Boolean, default=True)

    # Relación con el modelo Document
    documents = relationship("Document", back_populates="user")

    # Relación con el modelo Query
    queries = relationship("Query", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"

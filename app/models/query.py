from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base  # Importa Base desde base.py

class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String(255), nullable=False)
    answer = Column(String(255), nullable=False)
    context = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relación con el modelo User
    user = relationship("User", back_populates="queries")

    def __repr__(self):
        return f"<Query {self.query}>"

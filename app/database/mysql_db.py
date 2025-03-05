from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings

# Crear motor de base de datos
SQLALCHEMY_DATABASE_URL = settings.MYSQL_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """Generador de sesiones para la base de datos MySQL."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

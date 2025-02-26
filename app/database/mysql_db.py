from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base import Base  # Importa Base desde base.py
from app.models.user import User  # Importa el modelo User
from app.models.document import Document  # Importa el modelo Document
from app.models.query import Query  # Importa el modelo Query

# Configuración de la conexión a MySQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://app_user:app_password@mysql/app_db"

# Crear el motor de SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear una sesión local para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas automáticamente al iniciar la aplicación
Base.metadata.create_all(bind=engine)

# Función para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

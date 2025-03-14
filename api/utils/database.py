from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from config.settings import settings

# Configuración de MySQL
SQLALCHEMY_DATABASE_URL = settings.DB_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Configuración de MongoDB
mongo_client = MongoClient(settings.MONGO_URL)
mongo_db = mongo_client["rag_db"]  # Base de datos MongoDB

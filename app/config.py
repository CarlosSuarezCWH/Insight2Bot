import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Cargar el archivo .env
load_dotenv()

class Config:
    TEMP_PDF_PATH = "/tmp/pdf_uploads"  # Ruta temporal para almacenar archivos PDF

class Settings(BaseSettings):
    # Configuración de MySQL
    DB_HOST: str = os.getenv("DB_HOST", " 0.0.0.0:3306")  # Host de la base de datos MySQL
    DB_USER: str = os.getenv("DB_USER", "app_user")  # Usuario de la base de datos MySQL
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "app_password")  # Contraseña de la base de datos MySQL
    DB_NAME: str = os.getenv("DB_NAME", "app_db")  # Nombre de la base de datos MySQL

    # Configuración de MongoDB
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://mongo:27017")  # URI de conexión a MongoDB

    # Configuración de JWT (JSON Web Token)
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecretkey")  # Clave secreta para JWT
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")  # Algoritmo para JWT

    # Configuración de Ollama (si es necesario)
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://ollama:11434")  # Host de Ollama

    # Configuración de Redis (si es necesario)
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")  # Host de Redis
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))  # Puerto de Redis

# Instancia de configuración
settings = Settings()

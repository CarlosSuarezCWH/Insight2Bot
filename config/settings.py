# config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str = "mysql+pymysql://user:password@mysql:3306/rag_db"
    MONGO_URL: str = "mongodb://mongo:27017"
    JWT_SECRET: str = "supersecretkey"
    JWT_ALGORITHM: str = "HS256"
    OLLAMA_URL: str = "http://ollama:11434"

    class Config:
        env_file = ".env"

# Instancia global de settings
settings = Settings()

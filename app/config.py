from pydantic import BaseSettings

class Settings(BaseSettings):
    """Configuración de la aplicación, cargada desde variables de entorno."""

    # Configuración de base de datos MySQL
    MYSQL_DATABASE_URL: str
    MYSQL_DATABASE_NAME: str

    # Configuración de base de datos MongoDB
    MONGO_DATABASE_URL: str
    MONGO_DATABASE_NAME: str

    # Configuración JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int

    # Otros parámetros de configuración
    TEMP_PDF_PATH: str

    class Config:
        """Cargar variables de entorno desde un archivo .env"""
        env_file = ".env"

settings = Settings()

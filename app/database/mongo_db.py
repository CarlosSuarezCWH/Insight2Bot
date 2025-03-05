from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

# Crear cliente de MongoDB
mongo_client = AsyncIOMotorClient(settings.MONGO_DATABASE_URL)

# Seleccionar la base de datos
mongo_db = mongo_client[settings.MONGO_DATABASE_NAME]

def get_mongo_db():
    """Proporciona acceso a la base de datos MongoDB."""
    return mongo_db

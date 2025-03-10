from api.utils.database import engine, Base
from api.models.user import User
from api.models.document import Document
import faiss
import os

# Crear tablas en la base de datos
print("Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("Tablas creadas exitosamente.")

# Cargar o crear el índice FAISS
faiss_index_path = "/app/faiss_index/faiss_index.idx"
if os.path.exists(faiss_index_path):
    print("Cargando índice FAISS desde disco...")
    index = faiss.read_index(faiss_index_path)
else:
    print("Creando nuevo índice FAISS...")
    dimension = 384
    index = faiss.IndexFlatL2(dimension)
    faiss.write_index(index, faiss_index_path)

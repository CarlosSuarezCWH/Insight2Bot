from sentence_transformers import SentenceTransformer
import numpy as np

# Cargar el modelo una vez al iniciar la aplicación
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str):
    """
    Genera un embedding para el texto dado.
    """
    return model.encode(text)

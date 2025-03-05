FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt y los archivos de tu aplicación
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia todo el proyecto al contenedor
COPY ./app /app

# Expone el puerto 8000
EXPOSE 8000

# Ejecuta Uvicorn
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

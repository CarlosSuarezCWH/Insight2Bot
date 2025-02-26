# Usar una imagen base ligera
FROM python:3.9-slim-buster

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar los archivos de requisitos e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=2000 -r requirements.txt

# Copiar el resto del código
COPY . .

# Crear un usuario no root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Exponer el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

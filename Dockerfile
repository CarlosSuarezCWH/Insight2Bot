# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de dependencias de Python
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --default-timeout=2000 -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear un usuario no root para mayor seguridad
RUN useradd -m appuser && chown -R appuser:appuser /app

# Cambiar al usuario no root
USER appuser

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

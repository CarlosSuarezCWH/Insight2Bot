FROM python:3.9-slim
WORKDIR /app

# Copiar requirements.txt primero para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar wait-for-it.sh y dar permisos de ejecución
COPY wait-for-it.sh .
RUN chmod +x wait-for-it.sh

# Copiar todo el proyecto
COPY . .

# Establecer PYTHONPATH para que Python pueda encontrar el módulo `api`
ENV PYTHONPATH="${PYTHONPATH}:/app"



# Eliminar el CMD aquí porque ya lo pusimos en docker-compose.yml

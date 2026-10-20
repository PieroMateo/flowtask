FROM python:3.14-slim

# No generar archivos .pyc y mostrar los logs al instante (sin buffer).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Primero solo las dependencias: esta capa queda en caché mientras requirements.txt no cambie.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Carpeta donde vivirá flowtask.db (se monta como volumen en docker-compose).
RUN mkdir -p /app/data

EXPOSE 8000

# 0.0.0.0: aceptar conexiones desde fuera del contenedor, no solo desde él mismo.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

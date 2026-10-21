FROM python:3.14-slim

# sin archivos .pyc y con los logs saliendo al momento
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# primero solo requirements, asi docker reusa esta capa si las librerias no cambiaron
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# sqlite crea el archivo de la bd pero no la carpeta, por eso se crea aqui
RUN mkdir -p /app/data

EXPOSE 8000

# con 0.0.0.0 se puede entrar desde fuera del contenedor, con 127.0.0.1 no
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.10-slim

WORKDIR /app

# Copiar dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación y el módulo de observabilidad
COPY . .

# Exponer puerto referencial y arrancar leyendo la variable dinámica $PORT de Render
EXPOSE 10000
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-10000}"]

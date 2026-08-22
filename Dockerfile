# Imagen base de Python
FROM python:3.12-slim

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Puerto que usa Flask
EXPOSE 5000

# Ejecutar la app Flask con Gunicorn
CMD ["gunicorn", "--preload", "--config", "gunicorn.conf.py", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]
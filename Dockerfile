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

# Puerto que usa Streamlit
EXPOSE 8501

# Ejecutar Streamlit
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
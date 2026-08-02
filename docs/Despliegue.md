# Despliegue del Proyecto utilizando Docker

## Portada
* **Universidad:** Universidad Gerardo Barrios
* **Carrera:** Ingeniería en Sistemas y Redes Informáticas
* **Asignatura:** Desarrollo de Aplicaciones con IA
* **Proyecto:** Sistema Inteligente de Ciberseguridad para la Detección de Intrusiones Web
* **Integrante:** 
Merary Julissa Araujo Velásquez
Gilmar Adriel González Romero
Nathaly Saraí Rodriguez Silva
* **Docente:** Ingeniero Marcos Arevalo
* **Fecha:** 01 de agosto de 2026

---

## 1. Descripción breve del servicio preparado

El proyecto consiste en un sistema inteligente de ciberseguridad desarrollado para analizar solicitudes HTTP y detectar posibles comportamientos maliciosos mediante técnicas de Inteligencia Artificial.

La aplicación ofrece una interfaz web desarrollada con Streamlit que permite visualizar métricas, generar predicciones sobre posibles ataques y mostrar información relacionada con el monitoreo del tráfico web. Para facilitar su ejecución en cualquier entorno, el proyecto fue empaquetado utilizando Docker, permitiendo ejecutar todos los componentes dentro de un contenedor sin necesidad de instalar manualmente las dependencias.

---

## 2. Ruta elegida

* **Ruta seleccionada:** Docker

El despliegue se realizó mediante Docker Desktop utilizando un contenedor basado en Python 3.12, donde se instalaron automáticamente todas las dependencias definidas en el archivo [`requirements.txt`](/requirements.txt) y posteriormente se ejecutó la aplicación Streamlit.

---

## 3. Dockerfile utilizado

El archivo de configuración principal para la creación de la imagen se encuentra disponible en la raíz del proyecto:

📄 **[Ver Dockerfile](/Dockerfile)**

### Explicación de las directivas principales
* `FROM python:3.12-slim`: Utiliza una imagen ligera de Python 3.12.
* `WORKDIR /app`: Establece el directorio de trabajo dentro del contenedor.
* `COPY requirements.txt .`: Copia el archivo de dependencias al contenedor.
* `RUN pip install`: Instala automáticamente todas las librerías requeridas.
* `COPY . .`: Copia el código fuente del proyecto al contenedor.
* `EXPOSE 8501`: Expone el puerto utilizado por Streamlit.
* `CMD`: Inicia automáticamente la aplicación al ejecutar el contenedor.

---

## 4. Archivo .dockerignore

Para optimizar el tamaño de la imagen y excluir archivos no requeridos, se configuró el archivo de exclusiones:

📄 **[Ver .dockerignore](/.dockerignore)**

### Explicación de las exclusiones
Se excluyeron archivos y carpetas que no son necesarios para la ejecución del proyecto dentro del contenedor con el objetivo de reducir el tamaño de la imagen y mejorar el rendimiento durante la construcción.

| Archivo o carpeta | Motivo |
| :--- | :--- |
| `.venv/`, `venv/` | Entornos virtuales locales. |
| `__pycache__/` | Archivos temporales generados por Python. |
| `.git/` | Historial del repositorio Git. |
| `.github/` | Configuración de GitHub Actions. |
| `.vscode/` | Configuración local del editor Visual Studio Code. |
| `.env` | Contiene información sensible como claves de acceso. |
| `.pytest_cache/` | Caché de pruebas automatizadas. |
| `*.ipynb` | Notebooks utilizados durante el desarrollo. |
| `*.log` | Archivos de registro. |

---

## 5. Resultado del despliegue

El despliegue fue exitoso utilizando Docker Desktop. La aplicación quedó ejecutándose dentro de un contenedor Docker y fue accesible mediante la siguiente dirección local:

```text
http://localhost:8501
# Registro de errores, correcciones y bloqueos

## Proyecto

**Nombre del proyecto:** SOC-AI
**Tipo de proyecto:** API inteligente para la detección de anomalías en tráfico web
**Tecnología principal:** FastAPI, Python y Machine Learning
**Modelo utilizado:** Isolation Forest

---

## 1. Error en la ejecución inicial de las pruebas automatizadas

### Descripción del problema

Durante la primera ejecución del pipeline de integración continua mediante GitHub Actions, las pruebas no pudieron ejecutarse correctamente.

El resultado inicial mostraba un error similar a:

```text
collected 0 items / 1 error
```

Esto indicaba que el framework de pruebas `pytest` no estaba logrando recopilar y ejecutar correctamente las pruebas del proyecto.

### Posible causa

El problema estaba relacionado con la configuración inicial del entorno de pruebas y la estructura del proyecto. La ejecución del pipeline debía configurarse correctamente para:

* Descargar el código del repositorio.
* Configurar la versión de Python.
* Instalar las dependencias del proyecto.
* Ejecutar correctamente `pytest`.

### Corrección realizada

Se revisó la estructura del repositorio y la configuración del pipeline de GitHub Actions.

Se verificó que el archivo `requirements.txt` se encontrara en la raíz del proyecto y que el pipeline utilizara la ruta correcta:

```bash
pip install -r requirements.txt
```

También se configuró la ejecución de las pruebas mediante:

```bash
pytest
```

### Resultado

Después de revisar y corregir la configuración, el pipeline logró ejecutar correctamente las pruebas automatizadas.

El resultado exitoso se identificó mediante la ejecución correcta de las pruebas y la finalización satisfactoria del pipeline.

---

## 2. Error de documentación de la API en Swagger

### Descripción del problema

Después de realizar el primer despliegue de la API en Render, al acceder a la documentación interactiva mediante:

```text
https://soc-ai-api.onrender.com/docs
```

Swagger mostró el siguiente error:

```text
Failed to load API definition.
Fetch error
response status is 404 /openapi.json
```

### Análisis del problema

La interfaz `/docs` de FastAPI utiliza el archivo generado automáticamente:

```text
/openapi.json
```

para obtener la definición de los endpoints de la API.

Inicialmente, la interfaz de Swagger no pudo cargar correctamente esta definición.

### Verificación realizada

Se revisó el archivo principal de la API:

```text
API/main.py
```

y se confirmó que la aplicación estaba correctamente definida mediante:

```python
app = FastAPI(
    title="SOC-AI API",
    description="API de detección inteligente de anomalías en tráfico web",
    version="2.0.0"
)
```

También se verificó que no se habían desactivado las rutas de documentación mediante:

```python
docs_url=None
```

o:

```python
openapi_url=None
```

### Corrección y verificación

Se revisaron los logs de Render y se confirmó que la aplicación se estaba ejecutando correctamente mediante:

```bash
uvicorn API.main:app --host 0.0.0.0 --port $PORT
```

Posteriormente se verificó directamente la URL:

```text
https://soc-ai-api.onrender.com/openapi.json
```

La API respondió correctamente con la definición OpenAPI de la aplicación.

### Resultado

La documentación interactiva de FastAPI quedó disponible correctamente en:

```text
https://soc-ai-api.onrender.com/docs
```

Este proceso permitió comprobar que la API se encontraba correctamente desplegada y que sus endpoints estaban disponibles.

---

## 3. Advertencia de incompatibilidad de versión de scikit-learn

### Descripción del problema

Durante el despliegue de la API en Render se generaron advertencias relacionadas con la versión de `scikit-learn`.

El sistema mostró mensajes similares a:

```text
InconsistentVersionWarning:
Trying to unpickle estimator from version 1.8.0
when using version 1.9.0
```

### Causa

El modelo de Machine Learning fue entrenado y guardado utilizando una versión de `scikit-learn` diferente a la versión instalada durante el despliegue.

El modelo había sido creado con una versión anterior, mientras que Render instaló una versión más reciente debido a que la dependencia no estaba fijada a una versión específica.

### Riesgo identificado

Los archivos serializados del modelo, como:

```text
isolation_forest_model.pkl
scaler.pkl
label_encoder_metodo.pkl
```

pueden presentar problemas de compatibilidad si se cargan utilizando versiones diferentes de las bibliotecas con las que fueron creados.

### Corrección recomendada

Se recomienda especificar la versión utilizada durante el entrenamiento del modelo en el archivo:

```text
requirements.txt
```

Por ejemplo:

```text
scikit-learn==1.8.0
```

Esto permite que el entorno de ejecución utilice la misma versión de la biblioteca con la que fueron generados los modelos.

### Estado

**Estado:** Identificado y documentado.

La advertencia no impidió el inicio de la API, pero se considera una mejora necesaria para garantizar una mayor reproducibilidad y estabilidad del sistema.

---

## 4. Error relacionado con la ubicación de los archivos del modelo

### Descripción del problema

La API necesita cargar varios archivos de Machine Learning durante su inicio:

```text
isolation_forest_model.pkl
scaler.pkl
label_encoder_metodo.pkl
```

Inicialmente, existía el riesgo de que las rutas relativas utilizadas para cargar estos archivos no funcionaran correctamente en el entorno de despliegue.

### Causa

Las rutas relativas pueden comportarse de manera diferente dependiendo de la carpeta desde la cual se ejecuta la aplicación.

Una ruta como:

```python
"../modelo_guardado/isolation_forest_model.pkl"
```

puede provocar errores si el directorio de ejecución cambia.

### Corrección realizada

Se utilizó `pathlib` para construir las rutas a partir de la ubicación real del archivo `main.py`:

```python
BASE_DIR = Path(__file__).resolve().parent.parent
MODELO_DIR = BASE_DIR / "modelo_guardado"
```

Posteriormente, los modelos se cargan mediante:

```python
modelo = joblib.load(
    MODELO_DIR / "isolation_forest_model.pkl"
)
```

De esta forma, la aplicación utiliza rutas más confiables y menos dependientes del directorio actual de ejecución.

### Resultado

La API logró cargar correctamente los modelos durante el despliegue en Render.

Los logs confirmaron que la aplicación pudo iniciar correctamente:

```text
Application startup complete.
```

---

## 5. Error inicial de acceso a la ruta raíz de la API

### Descripción del problema

Al acceder directamente a:

```text
https://soc-ai-api.onrender.com/
```

se obtuvo una respuesta:

```text
404 Not Found
```

### Causa

La aplicación no tenía definido un endpoint para la ruta raíz:

```text
/
```

La API sí tenía endpoints específicos como:

```text
/health
/metadata
/analyze
```

pero no se había creado una función para responder a:

```text
/
```

### Análisis

Este comportamiento no representa necesariamente un error en la aplicación.

Una respuesta `404 Not Found` en la ruta raíz significa que no existe un endpoint definido para esa URL.

La API puede continuar funcionando correctamente mediante sus rutas específicas.

### Verificación

Se verificó que la API respondía correctamente mediante:

```text
/health
```

y:

```text
/metadata
```

También se comprobó que la documentación OpenAPI funcionaba correctamente mediante:

```text
/docs
```

### Resultado

El problema fue identificado como un comportamiento esperado debido a la ausencia de un endpoint raíz.

La funcionalidad principal de la API no se vio afectada.

---

## 6. Bloqueo relacionado con la conexión del repositorio a Render

### Descripción del problema

Al intentar crear el servicio en Render, inicialmente no aparecían los repositorios disponibles.

La plataforma mostraba un mensaje similar a:

```text
No repositories found
```

### Causa

Render todavía no tenía permisos para acceder al proveedor Git utilizado por el proyecto.

### Corrección realizada

Se configuró la conexión entre Render y el repositorio del proyecto.

Después de autorizar el acceso, el repositorio:

```text
ProyectoCiberseguridad
```

pudo ser encontrado y seleccionado para el despliegue.

### Resultado

Render logró conectarse correctamente al repositorio y utilizar el código del proyecto para crear el servicio web.

---

## 7. Configuración del directorio raíz del proyecto

### Situación identificada

El archivo:

```text
requirements.txt
```

se encuentra en la raíz del repositorio.

La estructura general del proyecto incluye:

```text
ProyectoCiberseguridad/
│
├── requirements.txt
│
├── API/
│   ├── main.py
│   └── schemas.py
│
├── modelo_guardado/
│
└── .github/
    └── workflows/
        └── ci.yml
```

### Decisión de configuración

Debido a que `requirements.txt` está en la raíz del proyecto, el campo:

```text
Root Directory
```

se dejó vacío.

El comando de instalación utilizado fue:

```bash
pip install -r requirements.txt
```

### Comando de inicio

Como la aplicación principal se encuentra en:

```text
API/main.py
```

y la instancia de FastAPI se llama:

```python
app
```

se utilizó:

```bash
uvicorn API.main:app --host 0.0.0.0 --port $PORT
```

### Resultado

Render pudo encontrar correctamente la aplicación, instalar sus dependencias y ejecutar el servidor Uvicorn.

---

## 8. Validación del despliegue

Después de corregir y verificar la configuración, Render mostró:

```text
Build successful
```

y posteriormente:

```text
Your service is live
```

La API quedó disponible públicamente mediante:

```text
https://soc-ai-api.onrender.com
```

La documentación interactiva quedó disponible mediante:

```text
https://soc-ai-api.onrender.com/docs
```

También se verificó la definición OpenAPI mediante:

```text
https://soc-ai-api.onrender.com/openapi.json
```

### Resultado final

El despliegue fue exitoso y la API pudo ser ejecutada fuera del entorno local.

---

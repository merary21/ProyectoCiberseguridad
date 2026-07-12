# Diagnóstico Técnico - Semana 1

## 1. Introducción

El presente documento tiene como finalidad describir el estado actual del proyecto **Sistema Inteligente de Detección de Anomalías en Aplicaciones Web con Inteligencia Artificial**, identificando las funcionalidades implementadas, las limitaciones existentes, las dependencias técnicas y los recursos necesarios para su funcionamiento.

Este diagnóstico servirá como punto de partida para planificar las mejoras que se desarrollarán durante las siguientes semanas del módulo, permitiendo evolucionar el prototipo hacia una solución más organizada, mantenible y preparada para un posible despliegue.

---

# 2. Estado actual del proyecto

Actualmente el proyecto se encuentra en la etapa de **prototipo funcional**. La aplicación ya es capaz de analizar registros de tráfico web utilizando Inteligencia Artificial para detectar comportamientos anómalos y mostrar los resultados mediante una interfaz web.

El sistema integra dos componentes principales de Inteligencia Artificial:

- Un modelo de Machine Learning basado en **Isolation Forest**, encargado de detectar anomalías dentro del tráfico web.
- Un asistente inteligente implementado mediante **Llama 3.2** ejecutado con **Ollama**, el cual responde consultas relacionadas con ciberseguridad.

Aunque la aplicación ya realiza las funciones principales para las cuales fue diseñada, aún existen componentes que requieren mejoras para cumplir con una arquitectura más robusta y preparada para producción.

---

# 3. Funcionalidades implementadas

Actualmente el sistema cuenta con las siguientes funcionalidades:

- Carga y procesamiento de registros de tráfico web.
- Análisis automático de los datos mediante el algoritmo Isolation Forest.
- Clasificación del tráfico como normal o anómalo.
- Generación de alertas cuando se detectan comportamientos sospechosos.
- Visualización de los resultados mediante una interfaz web desarrollada en Python.
- Consulta de métricas básicas del monitoreo.
- Integración con el asistente inteligente basado en Llama 3.2 utilizando Ollama.
- Respuestas automáticas a consultas relacionadas con ciberseguridad.
- Organización inicial del proyecto mediante carpetas y archivos de configuración.

Estas funcionalidades permiten demostrar que el prototipo cumple con su objetivo principal de apoyar el monitoreo inteligente de aplicaciones web.

---

# 4. Componentes incompletos o en desarrollo

Aunque el sistema ya funciona, aún existen componentes que requieren mejoras o todavía no han sido implementados.

Entre ellos se encuentran:

- Desarrollo de una API REST que permita separar el backend de la interfaz.
- Implementación de autenticación y control de acceso de usuarios.
- Integración con una base de datos para almacenar el historial de eventos.
- Automatización de pruebas unitarias.
- Configuración de integración continua (CI/CD).
- Implementación de Docker para facilitar el despliegue.
- Incorporación de métricas avanzadas y monitoreo mediante logs.
- Optimización del rendimiento del modelo de Inteligencia Artificial.

Estos elementos forman parte del plan de mejora definido para las siguientes semanas del módulo.

---

# 5. Dependencias técnicas

El funcionamiento del proyecto depende de diversas herramientas, bibliotecas y servicios.

## Lenguaje de programación

- Python 3.11 o superior.

## Bibliotecas principales

- Flask
- Pandas
- NumPy
- Scikit-Learn
- Joblib

## Inteligencia Artificial

- Isolation Forest.
- Llama 3.2.

## Servicios externos

- Ollama.

## Herramientas

- Git
- GitHub
- Visual Studio Code

Todas estas dependencias se encuentran registradas en el archivo **requirements.txt**, lo que facilita su instalación en nuevos entornos.

---

# 6. Datos, archivos y recursos necesarios

Para que el sistema funcione correctamente es necesario contar con los siguientes recursos.

## Dataset

El proyecto utiliza un conjunto de datos de tráfico web que sirve para entrenar y evaluar el modelo de detección de anomalías.

## Modelo entrenado

El modelo entrenado mediante Isolation Forest debe encontrarse disponible para realizar las predicciones.

## Archivos principales

- app.py
- requirements.txt
- .env
- Dataset (.csv)
- Modelo entrenado (.pkl)

## Servicios necesarios

- Ollama ejecutándose localmente.
- Modelo Llama 3.2 descargado.

La ausencia de alguno de estos recursos impediría el correcto funcionamiento de la aplicación.

---

# 7. Ejecución actual del proyecto

Actualmente la aplicación se ejecuta de forma local.

Para iniciar el sistema deben realizarse los siguientes pasos:

## Paso 1

Instalar las dependencias del proyecto.

```bash
pip install -r requirements.txt
```

## Paso 2

Descargar el modelo Llama 3.2.

```bash
ollama pull llama3.2
```

## Paso 3

Iniciar Ollama.

```bash
ollama serve
```

## Paso 4

Ejecutar la aplicación.

```bash
python app.py
```

Una vez iniciada, el usuario puede acceder a la interfaz web para cargar registros, analizar el tráfico y consultar el asistente inteligente.

---

# 8. Evidencias del funcionamiento

Actualmente se dispone de diferentes evidencias que demuestran el funcionamiento del prototipo.

Entre ellas se encuentran:

- Ejecución correcta de la aplicación.
- Interfaz web operativa.
- Detección de tráfico normal y anómalo.
- Alertas generadas por el modelo de Machine Learning.
- Respuestas proporcionadas por el asistente inteligente.
- Resultados obtenidos durante las pruebas realizadas por el equipo.

Como evidencia adicional se incluirán capturas de pantalla de la aplicación, diagramas de arquitectura y resultados de las pruebas realizadas durante el desarrollo del proyecto.

---

# 9. Conclusiones del diagnóstico

El análisis realizado permite concluir que el proyecto ya cuenta con una base funcional capaz de demostrar la integración de Inteligencia Artificial dentro de una aplicación web orientada al monitoreo de ciberseguridad.

Las principales funcionalidades relacionadas con el análisis inteligente del tráfico y el asistente conversacional ya se encuentran implementadas; sin embargo, todavía existen aspectos importantes por desarrollar, especialmente en temas de arquitectura, pruebas, despliegue, monitoreo y seguridad.

El diagnóstico realizado permitirá orientar el trabajo de las próximas semanas, priorizando aquellas mejoras que incrementen la calidad, mantenibilidad y escalabilidad del sistema hasta alcanzar la arquitectura objetivo definida para el proyecto.
